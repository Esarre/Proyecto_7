# Generated by Django 5.0.7 on 2024-07-25 15:30

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comuna",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comuna", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("region", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("rut", models.CharField(max_length=9, unique=True)),
                ("primer_nombre", models.CharField(max_length=15)),
                ("segundo_nombre", models.CharField(max_length=15)),
                ("apellido_paterno", models.CharField(max_length=15)),
                ("apellido_materno", models.CharField(max_length=15)),
                ("fecha_nac", models.DateField()),
                ("telefono", models.CharField(max_length=8, unique=True)),
                ("email", models.EmailField(max_length=30)),
                ("fecha_creacion", models.DateField(auto_now_add=True)),
                ("fecha_modificacion", models.DateField(auto_now=True)),
                (
                    "tipo_usuario",
                    models.CharField(
                        choices=[
                            ("administrador", "Administrador"),
                            ("arrendatario", "Arrendatario"),
                            ("arrendador", "Arrendador"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Inmueble",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=25)),
                ("descripcion", models.TextField()),
                ("m2_construidos", models.PositiveIntegerField()),
                ("m2_totales", models.PositiveIntegerField()),
                ("n_habitaciones", models.PositiveBigIntegerField()),
                ("n_banios", models.PositiveIntegerField()),
                ("n_estacionamientos", models.PositiveIntegerField()),
                ("precio", models.PositiveIntegerField()),
                ("fecha_creacion", models.DateField(auto_now_add=True)),
                ("fecha_modificacion", models.DateField(auto_now=True)),
                (
                    "tipo_inmueble",
                    models.CharField(
                        choices=[
                            ("casa", "Casa"),
                            ("departamento", "Departamento"),
                            ("parcela", "Parcela"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "arrendador_usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Imagen",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("imagen", models.ImageField(upload_to="Inmuebles/")),
                ("fecha_creacion", models.DateField(auto_now_add=True)),
                ("fecha_modificacion", models.DateField(auto_now=True)),
                (
                    "inmueble",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="imagenes",
                        to="inmobiliaria.inmueble",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Direccion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("calle", models.CharField(max_length=50)),
                ("numero", models.CharField(max_length=10)),
                ("numero_departamento", models.CharField(default=None, max_length=10)),
                ("fecha_creacion", models.DateField(auto_now_add=True)),
                (
                    "comuna",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inmobiliaria.comuna",
                    ),
                ),
                (
                    "inmueble",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inmobiliaria.inmueble",
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inmobiliaria.region",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comuna",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="inmobiliaria.region"
            ),
        ),
        migrations.CreateModel(
            name="SolicitudArriendo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha_solicitud", models.DateTimeField(auto_now_add=True)),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("pendiente", "Pendiente"),
                            ("aceptada", "Aceptada"),
                            ("rechazada", "Rechazada"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "inmueble",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inmobiliaria.inmueble",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="usuario",
            name="inmuebles_solicitados",
            field=models.ManyToManyField(
                related_name="solicitantes",
                through="inmobiliaria.SolicitudArriendo",
                to="inmobiliaria.inmueble",
            ),
        ),
    ]
