# Generated by Django 4.2.4 on 2023-08-30 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=83)),
                ('last_name', models.CharField(max_length=83)),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
            ],
            options={
                'ordering': ['departure_time'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('user', models.CharField(max_length=83)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=83)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TrainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=83)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=83)),
                ('cargo_num', models.IntegerField()),
                ('places_in_cargo', models.IntegerField()),
                ('train_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains', to='train.traintype')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.IntegerField()),
                ('seat', models.IntegerField()),
                ('journey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='train.journey')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='train.order')),
            ],
            options={
                'ordering': ['seat'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination', to='train.station')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source', to='train.station')),
            ],
            options={
                'ordering': ['-distance'],
            },
        ),
        migrations.AddField(
            model_name='journey',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to='train.route'),
        ),
        migrations.AddField(
            model_name='journey',
            name='train',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='journeys', to='train.train'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('cargo', 'seat', 'journey'), name='unique_cargo_seat_journey'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('cargo', 'seat', 'journey')},
        ),
    ]