
from typing import TypedDict

from django.db import transaction
from common.exceptions import APIValidationError

from polls.models import Poll, PollQuestion
from polls.services.question import QuestionServices


class NormalizedOptionPayload(TypedDict):
    name: str
    order: int


class NormalizedQuestionPayload(TypedDict):
    name: str
    description: str
    options: list[NormalizedOptionPayload]


class NormalizedPollPayload(TypedDict):
    name: str
    description: str
    status: Poll.Status
    result_visibility: Poll.ResultVisibility
    questions: list[NormalizedQuestionPayload]


class PollServices:

    @staticmethod
    def validate_and_normalize_payload(
        poll_data: dict,
    ) -> NormalizedPollPayload:

        if not isinstance(poll_data, dict):
            raise APIValidationError({
                'poll': 'The poll payload must be an object.'
            })

        # 1. Validate and normalize poll name.
        name = poll_data.get('name')

        if not isinstance(name, str) or not name.strip():
            raise APIValidationError({
                'name': 'A poll name is required.'
            })

        name = name.strip().lower()

        if Poll.objects.filter(name=name).exists():
            raise APIValidationError({
                'name': f"A poll with the name '{name}' already exists."
            })

        # 2. Validate poll description.
        description = poll_data.get('description', '')

        if not isinstance(description, str):
            raise APIValidationError({
                'description': 'Description must be a string.'
            })

        # 3. Normalize model choice values.
        def normalize_choice(field, value, choices, default):
            if value is None or value == '':
                value = default

            allowed_choices = {}

            for choice_value, label in choices:
                allowed_choices[str(choice_value).strip().casefold()] = (
                    choice_value
                )
                allowed_choices[str(label).strip().casefold()] = (
                    choice_value
                )

            normalized_value = str(value).strip().casefold()

            if normalized_value not in allowed_choices:
                raise APIValidationError({
                    field: 'Invalid choice value.'
                })

            return allowed_choices[normalized_value]

        status = Poll.Status(
            normalize_choice(
                'status',
                poll_data.get('status'),
                Poll.Status.choices,
                Poll.Status.DRAFT,
            )
        )

        result_visibility = Poll.ResultVisibility(
            normalize_choice(
                'result_visibility',
                poll_data.get('result_visibility'),
                Poll.ResultVisibility.choices,
                Poll.ResultVisibility.AFTER_SUBMISSION,
            )
        )

        # 4. Validate all questions and their options.
        questions_data = poll_data.get('questions', [])

        if not isinstance(questions_data, list):
            raise APIValidationError({
                'questions': 'Questions must be a list.'
            })

        normalized_questions: list[NormalizedQuestionPayload] = []
        seen_question_names = set()

        for question_index, question_data in enumerate(questions_data):

            if not isinstance(question_data, dict):
                raise APIValidationError({
                    'questions': (
                        f'Question at index {question_index} must be an object.'
                    )
                })

            question_name = question_data.get('name')

            if not isinstance(question_name, str) or not question_name.strip():
                raise APIValidationError({
                    'questions': (
                        f'A valid name is required for question '
                        f'at index {question_index}.'
                    )
                })

            question_name = question_name.strip().lower()

            if question_name in seen_question_names:
                raise APIValidationError({
                    'questions': (
                        f"Duplicate question name '{question_name}'."
                    )
                })

            seen_question_names.add(question_name)

            question_description = question_data.get('description', '')

            if not isinstance(question_description, str):
                raise APIValidationError({
                    'questions': (
                        f"Description for '{question_name}' must be a string."
                    )
                })

            options_data = question_data.get('options', [])

            if not isinstance(options_data, list):
                raise APIValidationError({
                    'options': (
                        f"Options for '{question_name}' must be a list."
                    )
                })

            normalized_options: list[NormalizedOptionPayload] = []
            seen_option_names = set()

            for option_index, option_data in enumerate(options_data):

                if not isinstance(option_data, dict):
                    raise APIValidationError({
                        'options': (
                            f'Option at index {option_index} for '
                            f"'{question_name}' must be an object."
                        )
                    })

                option_name = option_data.get('name')

                if not isinstance(option_name, str) or not option_name.strip():
                    raise APIValidationError({
                        'options': (
                            f'A valid option name is required for '
                            f"'{question_name}'."
                        )
                    })

                option_name = option_name.strip()
                normalized_option_name = option_name.casefold()

                if normalized_option_name in seen_option_names:
                    raise APIValidationError({
                        'options': (
                            f"Duplicate option name '{option_name}' "
                            f"for question '{question_name}'."
                        )
                    })

                seen_option_names.add(normalized_option_name)

                option_order = option_data.get('order', option_index + 1)

                if (
                    isinstance(option_order, bool)
                    or not isinstance(option_order, int)
                    or option_order < 1
                ):
                    raise APIValidationError({
                        'options': (
                            f"Order for option '{option_name}' "
                            'must be a positive integer.'
                        )
                    })

                normalized_options.append({
                    'name': option_name,
                    'order': option_order,
                })

            normalized_questions.append({
                'name': question_name,
                'description': question_description.strip(),
                'options': normalized_options,
            })

        return {
            'name': name,
            'description': description.strip(),
            'status': status,
            'result_visibility': result_visibility,
            'questions': normalized_questions,
        }

    @staticmethod
    def create_poll(
        user,
        name: str,
        description: str = '',
        status: Poll.Status = Poll.Status.DRAFT,
        result_visibility: Poll.ResultVisibility = (
            Poll.ResultVisibility.AFTER_SUBMISSION
        ),
    ) -> Poll:

        return Poll.objects.create(
            name=name,
            description=description,
            status=status,
            result_visibility=result_visibility,
            created_by=user,
        )

    @staticmethod
    def mega_poll(poll_data: dict, user=None) -> Poll:

        with transaction.atomic():

            # Centralized validation and normalization.
            normalized_data = (
                PollServices.validate_and_normalize_payload(poll_data)
            )

            # 1. Create the poll.
            created_poll = PollServices.create_poll(
                user=user,
                name=normalized_data['name'],
                description=normalized_data['description'],
                status=normalized_data['status'],
                result_visibility=normalized_data['result_visibility'],
            )

            # 2. Bulk-upsert questions and their answer options.
            created_questions = QuestionServices.bulk_create_questions(
                user=user,
                questions_data=normalized_data['questions'],
            )

            # 3. Create PollQuestion relationships.
            poll_question_rows = [
                PollQuestion(
                    poll=created_poll,
                    question_id=question_data['id'],
                    order=index,
                )
                for index, question_data in enumerate(created_questions)
            ]

            PollQuestion.objects.bulk_create(
                poll_question_rows,
                ignore_conflicts=True,
            )

            # 4. Attach the questions and their options to the poll object.
            created_poll.questions_data = created_questions

            return created_poll
