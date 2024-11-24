# Generated by Django 5.1.1 on 2024-09-29 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("comment_count", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("username", models.CharField(max_length=255, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("bio", models.TextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PostTag",
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
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.post"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.tag"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                related_name="posts", through="blog.PostTag", to="blog.tag"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="blog.user"
            ),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.post"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.user"
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="posttag",
            index=models.Index(
                fields=["post", "tag"], name="blog_postta_post_id_68f723_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="posttag",
            index=models.Index(fields=["tag"], name="blog_postta_tag_id_706589_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="posttag",
            unique_together={("post", "tag")},
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["author"], name="blog_post_author__038a48_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["created_date"], name="blog_post_created_f06acf_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["post", "created_date"], name="blog_commen_post_id_ef043e_idx"
            ),
        ),
    ]
