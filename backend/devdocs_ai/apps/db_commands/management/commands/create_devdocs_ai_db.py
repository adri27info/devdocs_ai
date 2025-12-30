import traceback

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

from apps.users.models import User
from apps.plans_types.models import PlanType
from apps.formats.models import Format
from apps.plans_types_formats.models import PlanTypeFormat
from apps.roles_projects.models import RoleProject
from apps.roles.models import Role
from apps.llms.models import LLM

from utils.general_utils import GeneralUtils
from utils.logger_utils import LoggerUtils
from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.services.user.create.user_create_image_setter_service \
    import UserCreateImageSetterService

LOGGER = LoggerUtils().get_logger()


class Command(BaseCommand):
    """
    Create the database, run migrations, and seed initial data.
    """

    def handle(self, *args, **kwargs):
        """
        Execute migrations and seed initial data.
        """
        self.execute_migrations()
        self.seed_initial_data()

    def execute_migrations(self):
        """
        Run Django's makemigrations and migrate commands.
        """
        LOGGER.info("Running makemigrations...")
        call_command("makemigrations")

        LOGGER.info("Running migrate...")
        call_command("migrate")

    def seed_initial_data(self):
        """
        Seed initial database data inside a transaction.
        """
        LOGGER.info("Seeding initial data...")

        try:
            with transaction.atomic():
                self.check_if_env_vars_exists()
                self.create_llm_model()
                self.create_roles()
                self.create_formats()
                self.create_plan_types()
                self.create_plan_type_formats()
                self.create_users()
                self.create_role_project()
        except Exception as e:
            LOGGER.error(f"Error during initial data seeding: {e}")
            LOGGER.error(traceback.format_exc())
            return

        LOGGER.info("Database setup and seeding completed!")

    def check_if_env_vars_exists(self):
        """
        Check that required environment variables are set.

        Raises:
            InstanceInvalidValueException: If EMAIL_HOST_USER or OPENROUTER_MODEL is missing.
        """
        if not settings.EMAIL_HOST_USER:
            raise InstanceInvalidValueException(
                "EMAIL_HOST_USER is missing or invalid"
            )

        if not settings.OPENROUTER_MODEL:
            raise InstanceInvalidValueException(
                "OPENROUTER_MODEL is missing or invalid"
            )

    def create_llm_model(self):
        """
        Create LLM model if it doesn't exist.
        """
        openrouter_model = settings.OPENROUTER_MODEL
        llm_model_data = {
            "name": openrouter_model,
            "description": (
                "A high-performing, industry-standard 7.3B parameter model, with "
                "optimizations for speed and context length. Mistral 7B Instruct "
                "has multiple version variants, and this is intended to be the "
                "latest version."
            ),
            "url": f"https://openrouter.ai/{openrouter_model}",
        }

        llm_model, created = LLM.objects.get_or_create(
            name=llm_model_data["name"],
            defaults=llm_model_data
        )

        if created:
            LOGGER.info(f"LLM Model '{llm_model.name}' was created successfully.")
        else:
            LOGGER.info(f"LLM Model '{llm_model.name}' already exists.")

    def create_roles(self):
        """
        Create default roles if they don't exist.
        """
        roles = ["admin", "user"]

        for role_name in roles:
            _, created = Role.objects.get_or_create(name=role_name)
            if created:
                LOGGER.info(f"{role_name} role was created successfully.")
            else:
                LOGGER.info(f"{role_name} role already exists.")

    def create_formats(self):
        """
        Create default formats if they don't exist.
        """
        formats = ["plain", "pdf"]

        for format_name in formats:
            _, created = Format.objects.get_or_create(name=format_name)
            if created:
                LOGGER.info(f"{format_name} format was created successfully.")
            else:
                LOGGER.info(f"{format_name} format already exists.")

    def create_plan_types(self):
        """
        Create default plan types if they don't exist.
        """
        plan_types = [
            {
                "name": "free",
                "max_projects": 2,
                "max_users": 1,
                "can_invite": False,
                "is_private_allowed": False
            },
            {
                "name": "premium",
                "max_projects": 5,
                "max_users": 3,
                "can_invite": True,
                "is_private_allowed": True
            }
        ]
        for plan_type in plan_types:
            _, created = PlanType.objects.get_or_create(
                name=plan_type["name"],
                max_projects=plan_type["max_projects"],
                max_users=plan_type["max_users"],
                can_invite=plan_type.get("can_invite", False),
                is_private_allowed=plan_type.get("is_private_allowed", False)
            )
            if created:
                LOGGER.info(
                    f"Plan type '{plan_type['name']}' was created successfully."
                )
            else:
                LOGGER.info(f"Plan type '{plan_type['name']}' already exists.")

    def create_plan_type_formats(self):
        """
        Create mappings between plan types and formats if they don't exist.
        """
        plan_format_data = [
            ("free", "plain"),
            ("premium", "plain"),
            ("premium", "pdf"),
        ]

        for plan_type_name, format_name in plan_format_data:
            plan_type = PlanType.objects.filter(name=plan_type_name).first()
            format = Format.objects.filter(name=format_name).first()

            if plan_type and format:
                _, created = PlanTypeFormat.objects.get_or_create(
                    plan_type=plan_type,
                    format=format
                )
                if created:
                    LOGGER.info(
                        f"The '{plan_type_name}' plan type with '{format_name}' format "
                        "was created successfully."
                    )
                else:
                    LOGGER.info(
                        f"The '{plan_type_name}' plan type with '{format_name}' format "
                        "already exists."
                    )
            else:
                LOGGER.info(
                    f"Either plan type '{plan_type_name}' or format '{format_name}' "
                    "does not exist."
                )

    def create_users(self):
        """
        Create default users if they don't exist.
        """
        default_plan_type_user = PlanType.objects.filter(name="free").first()
        role_admin = Role.objects.filter(name="admin").first()
        role_user = Role.objects.filter(name="user").first()
        password_users = "Test1ng_app"

        users = [
            {
                "email": settings.EMAIL_HOST_USER,
                "first_name": "Admin",
                "last_name": "Devdocs AI",
                "is_superuser": True,
                "is_staff": True,
                "plan_type": default_plan_type_user,
                "role": role_admin,
                "activation_code": GeneralUtils.generate_activation_code(),
            },
            {
                "email": "testuser1@example.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "is_superuser": False,
                "is_staff": False,
                "plan_type": default_plan_type_user,
                "role": role_user,
                "activation_code": GeneralUtils.generate_activation_code(),
            },
            {
                "email": "testuser2@example.com",
                "first_name": "John",
                "last_name": "Smith",
                "is_superuser": False,
                "is_staff": False,
                "plan_type": default_plan_type_user,
                "role": role_user,
                "activation_code": GeneralUtils.generate_activation_code(),
            },
            {
                "email": "testuser3@example.com",
                "first_name": "Peter",
                "last_name": "Jackson",
                "is_superuser": False,
                "is_staff": False,
                "plan_type": default_plan_type_user,
                "role": role_user,
                "activation_code": GeneralUtils.generate_activation_code(),
            },
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults=user_data
            )

            if created:
                user.set_password(password_users)
                user.save()

                UserCreateImageSetterService.run(user=user)
                LOGGER.info(f"User '{user.email}' created successfully.")
            else:
                LOGGER.info(f"User '{user.email}' already exists.")

    def create_role_project(self):
        """
        Create default project roles if they don't exist.
        """
        roles = ["owner", "member"]

        for role_name in roles:
            _, created = RoleProject.objects.get_or_create(name=role_name)
            if created:
                LOGGER.info(f"'{role_name}' role was created successfully.")
            else:
                LOGGER.info(f"'{role_name}' role already exists.")
