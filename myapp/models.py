from django.db import models

# Create your models here.


class Users(models.Model):
    pm = models.CharField(db_column='PM', primary_key=True, max_length=50)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=50, null=True, blank=True)  # Field name made lowercase.
    user_type = models.IntegerField(db_column='User_type', blank=True, null=True)  # Field name made lowercase.
    pwd = models.CharField(db_column='pwd', max_length=50, blank=True, null=True)
    eml = models.CharField(db_column='eml', max_length=50, blank=True, null=True)
    dept = models.CharField(db_column='dept', max_length=50, blank=True, null=True)


class Projects(models.Model):
    STATUS_CHOICES = [
        ('red','red'),
        ('yellow','yellow'),
        ('green','green'),
        ('grey','grey'),
    ]

    TYPE_CHOICES = {
        ('SPA','SPA'),
        ('PLP','PLP'),
    }

    projectid = models.AutoField(db_column='ProjectID', primary_key=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='Project_name', max_length=200)  # Field name made lowercase.
    pm = models.ForeignKey('Users', models.DO_NOTHING, db_column='PM', blank=True, null=True)  # Field name made lowercase.
    estimated_budget = models.IntegerField(db_column='Estimated_budget', blank=True, null=True)  # Field name made lowercase.
    irr = models.IntegerField(db_column='IRR', blank=True, null=True)  # Field name made lowercase.
    project_status = models.CharField(db_column='Project_status',choices=STATUS_CHOICES, max_length=10, default='green')  # Field name made lowercase.
    project_type = models.CharField(db_column='Project_type',choices=TYPE_CHOICES, max_length=30, blank=True, null=True)  # Field name made lowercase.
    project_manager = models.CharField(db_column='Project_manager', max_length=50, blank=True, null=True)  # Field name made lowercase.
    project_team = models.CharField(db_column='Project_team', max_length=200, blank=True, null=True)  # Field name made lowercase.
    timing_kickoff = models.DateField(db_column='Timing_kickoff', blank=True, null=True)  # Field name made lowercase.
    timing_closure = models.DateField(db_column='Timing_closure', blank=True, null=True)  # Field name made lowercase.
    timing_milestone1 = models.DateField(db_column='Timing_milestone1', blank=True, null=True)  # Field name made lowercase.
    timing_milestone2 = models.DateField(db_column='Timing_milestone2', blank=True, null=True)  # Field name made lowercase.
    timing_milestone3 = models.DateField(db_column='Timing_milestone3', blank=True, null=True)  # Field name made lowercase.
    timing_milestone4 = models.DateField(db_column='Timing_milestone4', blank=True, null=True)  # Field name made lowercase.
    main_target = models.CharField(db_column='Main_target', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    boundary_conditions = models.CharField(db_column='Boundary_conditions', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    out_of_scope = models.CharField(db_column='Out_of_scope', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    steering_committee = models.CharField(db_column='Steering_committee', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    facilitator = models.CharField(db_column='Facilitator', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    risk_uncertainties = models.CharField(db_column='Risk_uncertainties', max_length=2000, blank=True, null=True)  # Field name made lowercase.

class Test(models.Model):
    name = models.CharField(db_column='name', max_length=200)

class Announcement(models.Model):
    projectid = models.OneToOneField('Projects', on_delete=models.CASCADE, db_column='ProjectID', primary_key=True)  # Field name made lowercase.
    init_situation1 = models.TextField(db_column='Init_situation1', blank=True, null=True)  # Field name made lowercase.
    gene_concept1 = models.TextField(db_column='Gene_concept1', blank=True, null=True)  # Field name made lowercase.
    init_situation2 = models.TextField(db_column='Init_situation2', blank=True, null=True)  # Field name made lowercase.
    gene_concept2 = models.TextField(db_column='Gene_concept2', blank=True, null=True)  # Field name made lowercase.
    init_situation3 = models.TextField(db_column='Init_situation3', blank=True, null=True)  # Field name made lowercase.
    gene_concept3 = models.TextField(db_column='Gene_concept3', blank=True, null=True)  # Field name made lowercase.
    init_situation4 = models.TextField(db_column='Init_situation4', blank=True, null=True)  # Field name made lowercase.
    gene_concept4 = models.TextField(db_column='Gene_concept4', blank=True, null=True)  # Field name made lowercase.

class KickOff(models.Model):
    projectid = models.OneToOneField('Projects', on_delete=models.CASCADE, db_column='ProjectID', primary_key=True)  # Field name made lowercase.
    sub_target1 = models.TextField(db_column='Sub_target1', blank=True, null=True)  # Field name made lowercase.
    success_criteria1 = models.TextField(db_column='Success_criteria1', blank=True, null=True)  # Field name made lowercase.
    sub_target2 = models.TextField(db_column='Sub_target2', blank=True, null=True)  # Field name made lowercase.
    success_criteria2 = models.TextField(db_column='Success_criteria2', blank=True, null=True)  # Field name made lowercase.
    sub_target3 = models.TextField(db_column='Sub_target3', blank=True, null=True)  # Field name made lowercase.
    success_criteria3 = models.TextField(db_column='Success_criteria3', blank=True, null=True)  # Field name made lowercase.
    sub_target4 = models.TextField(db_column='Sub_target4', blank=True, null=True)  # Field name made lowercase.
    success_criteria4 = models.TextField(db_column='Success_criteria4', blank=True, null=True)  # Field name made lowercase.

class Milestones(models.Model):
    projectid = models.OneToOneField('Projects', on_delete=models.CASCADE, db_column='ProjectID', primary_key=True)  # Field name made lowercase.
    ppc_deliverable = models.CharField(db_column='PPC_deliverable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ppc_timing = models.CharField(db_column='PPC_timing', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ppc_budget = models.CharField(db_column='PPC_budget', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ppc_resources = models.CharField(db_column='PPC_resources', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ppc_risks = models.CharField(db_column='PPC_risks', max_length=1, blank=True, null=True)  # Field name made lowercase.
    deliverable_ms1 = models.TextField(db_column='Deliverable_ms1', blank=True, null=True)  # Field name made lowercase.
    deliverable_ms2 = models.TextField(db_column='Deliverable_ms2', blank=True, null=True)  # Field name made lowercase.
    deliverable_ms3 = models.TextField(db_column='Deliverable_ms3', blank=True, null=True)  # Field name made lowercase.
    deliverable_ms4 = models.TextField(db_column='Deliverable_ms4', blank=True, null=True)  # Field name made lowercase.
    deliverable_closure = models.TextField(db_column='Deliverable_closure', blank=True, null=True)  # Field name made lowercase.
    next_step = models.TextField(db_column='Next_step', blank=True, null=True)  # Field name made lowercase.

class Closure(models.Model):
    projectid = models.OneToOneField('Projects', on_delete=models.CASCADE, db_column='ProjectID', primary_key=True)  # Field name made lowercase.
    sub_target1 = models.TextField(db_column='Sub_target1', blank=True, null=True)  # Field name made lowercase.
    success_criteria1 = models.TextField(db_column='Success_criteria1', blank=True, null=True)  # Field name made lowercase.
    sub_target2 = models.TextField(db_column='Sub_target2', blank=True, null=True)  # Field name made lowercase.
    success_criteria2 = models.TextField(db_column='Success_criteria2', blank=True, null=True)  # Field name made lowercase.
    sub_target3 = models.TextField(db_column='Sub_target3', blank=True, null=True)  # Field name made lowercase.
    success_criteria3 = models.TextField(db_column='Success_criteria3', blank=True, null=True)  # Field name made lowercase.
    sub_target4 = models.TextField(db_column='Sub_target4', blank=True, null=True)  # Field name made lowercase.
    success_criteria4 = models.TextField(db_column='Success_criteria4', blank=True, null=True)  # Field name made lowercase.

