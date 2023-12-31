# Generated by Django 4.2.4 on 2023-08-11 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('projectid', models.AutoField(db_column='ProjectID', primary_key=True, serialize=False)),
                ('project_name', models.CharField(db_column='Project_name', max_length=200)),
                ('estimated_budget', models.IntegerField(blank=True, db_column='Estimated_budget', null=True)),
                ('irr', models.IntegerField(blank=True, db_column='IRR', null=True)),
                ('project_status', models.IntegerField(blank=True, db_column='Project_status', null=True)),
                ('project_type', models.CharField(blank=True, db_column='Project_type', max_length=30, null=True)),
                ('project_manager', models.CharField(blank=True, db_column='Project_manager', max_length=50, null=True)),
                ('project_team', models.CharField(blank=True, db_column='Project_team', max_length=200, null=True)),
                ('timing_kickoff', models.DateField(blank=True, db_column='Timing_kickoff', null=True)),
                ('timing_closure', models.DateField(blank=True, db_column='Timing_closure', null=True)),
                ('timing_milestone1', models.DateField(blank=True, db_column='Timing_milestone1', null=True)),
                ('timing_milestone2', models.DateField(blank=True, db_column='Timing_milestone2', null=True)),
                ('timing_milestone3', models.DateField(blank=True, db_column='Timing_milestone3', null=True)),
                ('timing_milestone4', models.DateField(blank=True, db_column='Timing_milestone4', null=True)),
                ('main_target', models.CharField(blank=True, db_column='Main_target', max_length=2000, null=True)),
                ('boundary_conditions', models.CharField(blank=True, db_column='Boundary_conditions', max_length=2000, null=True)),
                ('out_of_scope', models.CharField(blank=True, db_column='Out_of_scope', max_length=2000, null=True)),
                ('steering_committee', models.CharField(blank=True, db_column='Steering_committee', max_length=2000, null=True)),
                ('facilitator', models.CharField(blank=True, db_column='Facilitator', max_length=2000, null=True)),
                ('risk_uncertainties', models.CharField(blank=True, db_column='Risk_uncertainties', max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('pm', models.AutoField(db_column='PM', primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='Username', max_length=50)),
                ('user_type', models.IntegerField(blank=True, db_column='User_type', null=True)),
                ('pwd', models.CharField(blank=True, db_column='pwd', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('projectid', models.OneToOneField(db_column='ProjectID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.projects')),
                ('init_situation1', models.TextField(blank=True, db_column='Init_situation1', null=True)),
                ('gene_concept1', models.TextField(blank=True, db_column='Gene_concept1', null=True)),
                ('init_situation2', models.TextField(blank=True, db_column='Init_situation2', null=True)),
                ('gene_concept2', models.TextField(blank=True, db_column='Gene_concept2', null=True)),
                ('init_situation3', models.TextField(blank=True, db_column='Init_situation3', null=True)),
                ('gene_concept3', models.TextField(blank=True, db_column='Gene_concept3', null=True)),
                ('init_situation4', models.TextField(blank=True, db_column='Init_situation4', null=True)),
                ('gene_concept4', models.TextField(blank=True, db_column='Gene_concept4', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Closure',
            fields=[
                ('projectid', models.OneToOneField(db_column='ProjectID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.projects')),
                ('sub_target1', models.TextField(blank=True, db_column='Sub_target1', null=True)),
                ('success_criteria1', models.TextField(blank=True, db_column='Success_criteria1', null=True)),
                ('sub_target2', models.TextField(blank=True, db_column='Sub_target2', null=True)),
                ('success_criteria2', models.TextField(blank=True, db_column='Success_criteria2', null=True)),
                ('sub_target3', models.TextField(blank=True, db_column='Sub_target3', null=True)),
                ('success_criteria3', models.TextField(blank=True, db_column='Success_criteria3', null=True)),
                ('sub_target4', models.TextField(blank=True, db_column='Sub_target4', null=True)),
                ('success_criteria4', models.TextField(blank=True, db_column='Success_criteria4', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KickOff',
            fields=[
                ('projectid', models.OneToOneField(db_column='ProjectID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.projects')),
                ('sub_target1', models.TextField(blank=True, db_column='Sub_target1', null=True)),
                ('success_criteria1', models.TextField(blank=True, db_column='Success_criteria1', null=True)),
                ('sub_target2', models.TextField(blank=True, db_column='Sub_target2', null=True)),
                ('success_criteria2', models.TextField(blank=True, db_column='Success_criteria2', null=True)),
                ('sub_target3', models.TextField(blank=True, db_column='Sub_target3', null=True)),
                ('success_criteria3', models.TextField(blank=True, db_column='Success_criteria3', null=True)),
                ('sub_target4', models.TextField(blank=True, db_column='Sub_target4', null=True)),
                ('success_criteria4', models.TextField(blank=True, db_column='Success_criteria4', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('projectid', models.OneToOneField(db_column='ProjectID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.projects')),
                ('ppc_deliverable', models.CharField(blank=True, db_column='PPC_deliverable', max_length=1, null=True)),
                ('ppc_timing', models.CharField(blank=True, db_column='PPC_timing', max_length=1, null=True)),
                ('ppc_budget', models.CharField(blank=True, db_column='PPC_budget', max_length=1, null=True)),
                ('ppc_resources', models.CharField(blank=True, db_column='PPC_resources', max_length=1, null=True)),
                ('ppc_risks', models.CharField(blank=True, db_column='PPC_risks', max_length=1, null=True)),
                ('deliverable_ms1', models.TextField(blank=True, db_column='Deliverable_ms1', null=True)),
                ('deliverable_ms2', models.TextField(blank=True, db_column='Deliverable_ms2', null=True)),
                ('deliverable_ms3', models.TextField(blank=True, db_column='Deliverable_ms3', null=True)),
                ('deliverable_ms4', models.TextField(blank=True, db_column='Deliverable_ms4', null=True)),
                ('deliverable_closure', models.TextField(blank=True, db_column='Deliverable_closure', null=True)),
                ('next_step', models.TextField(blank=True, db_column='Next_step', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='pm',
            field=models.ForeignKey(blank=True, db_column='PM', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.users'),
        ),
    ]
