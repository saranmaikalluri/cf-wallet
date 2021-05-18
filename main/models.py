from django.db import models

# Create your models here.
class Student(models.Model):
    studentid = models.BigAutoField(db_column='StudentId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=500)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    photopath = models.CharField(db_column='PhotoPath', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=500)  # Field name made lowercase.
    dob = models.DateTimeField(db_column='DOB')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=15, blank=True, null=True)  # Field name made lowercase.
    phoneno = models.CharField(db_column='PhoneNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mobileno = models.CharField(db_column='MobileNo', max_length=50)  # Field name made lowercase.
    maritalstatus = models.CharField(db_column='MaritalStatus', max_length=20, blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.CharField(db_column='AddressLine1', max_length=1000)  # Field name made lowercase.
    addressline2 = models.CharField(db_column='AddressLine2', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=500)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=500)  # Field name made lowercase.
    countryid = models.IntegerField(db_column='CountryId')  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    partnerid = models.ForeignKey('main.Aspnetusers', models.DO_NOTHING, db_column='PartnerId')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='ModifiedOn', blank=True, null=True)  # Field name made lowercase.
    partnersstudentid = models.IntegerField(db_column='PartnersStudentId', blank=True, null=True)  # Field name made lowercase.
    staffid = models.TextField(db_column='StaffId', blank=True, null=True)  # Field name made lowercase.
    countrieschosen = models.CharField(db_column='CountriesChosen', max_length=100, blank=True, null=True)  # Field name made lowercase.
    studycountryid = models.IntegerField(db_column='StudyCountryId', blank=True, null=True)  # Field name made lowercase.
    higheststudylevelid = models.IntegerField(db_column='HighestStudyLevelId', blank=True, null=True)  # Field name made lowercase.
    studylevelidpassed = models.CharField(db_column='StudyLevelIdPassed', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Students'

class Universities(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    docid = models.TextField(db_column='DocId', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    country = models.IntegerField(db_column='Country')  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='ModifiedOn')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    tieup = models.BooleanField(db_column='TieUp')  # Field name made lowercase.
    displayorder = models.IntegerField(db_column='DisplayOrder')  # Field name made lowercase.
    backlogrange = models.TextField(db_column='BacklogRange', blank=True, null=True)  # Field name made lowercase.
    currency = models.TextField(db_column='Currency', blank=True, null=True)  # Field name made lowercase.
    webomatricsworldranking = models.IntegerField(db_column='WebomatricsWorldRanking', blank=True, null=True)  # Field name made lowercase.
    webomatricsnationalranking = models.IntegerField(db_column='WebomatricsNationalRanking', blank=True, null=True)  # Field name made lowercase.
    isindirect = models.BooleanField(db_column='IsIndirect')  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking', blank=True, null=True)  # Field name made lowercase.
    rankingfrom = models.TextField(db_column='RankingFrom', blank=True, null=True)  # Field name made lowercase.
    applicationmode = models.TextField(db_column='ApplicationMode', blank=True, null=True)  # Field name made lowercase.
    commissionmode = models.CharField(db_column='CommissionMode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    commissionvalue = models.DecimalField(db_column='CommissionValue', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extension = models.TextField(db_column='Extension', blank=True, null=True)  # Field name made lowercase.
    acceptedcurrencycode = models.TextField(db_column='AcceptedCurrencyCode', blank=True, null=True)  # Field name made lowercase.
    universitydetail = models.IntegerField(db_column='UniversityDetail_Id', blank=True, null=True)  # Field name made lowercase.
    bankdetails = models.TextField(db_column='Bankdetails', blank=True, null=True)  # Field name made lowercase.
    applicationfeemarkupvalue = models.DecimalField(db_column='ApplicationFeeMarkupValue', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Universities'

class Courses(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    university = models.CharField(db_column='University', max_length=450, blank=True, null=True)  # Field name made lowercase.
    countryid = models.IntegerField(db_column='CountryId')  # Field name made lowercase.
    universityid = models.IntegerField(db_column='UniversityId')  # Field name made lowercase.
    studylevelid = models.IntegerField(db_column='StudyLevelId')  # Field name made lowercase.
    categoryid = models.TextField(db_column='CategoryId', blank=True, null=True)  # Field name made lowercase.
    subcategoryid = models.TextField(db_column='SubCategoryId', blank=True, null=True)  # Field name made lowercase.
    campus = models.TextField(db_column='Campus', blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='ModifiedOn')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    displayorder = models.IntegerField(db_column='DisplayOrder')  # Field name made lowercase.
    concentration = models.TextField(db_column='Concentration', blank=True, null=True)  # Field name made lowercase.
    commissionmode = models.CharField(db_column='CommissionMode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    commissionvalue = models.DecimalField(db_column='CommissionValue', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    backlog = models.IntegerField(blank=True, null=True)
    coursedetail = models.IntegerField(db_column='CourseDetail_Id', blank=True, null=True)  # Field name made lowercase.
    isonlinecourse = models.BooleanField(db_column='IsOnlineCourse', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Courses'
        
class Acknowledgements(models.Model):
    acknowledgementid = models.AutoField(db_column='AcknowledgementId', primary_key=True)   
    acknowledgementnumber = models.CharField(db_column='AcknowledgementNumber', max_length=500, blank=True, null=True, verbose_name='Acknowledgement Number')   
    student = models.ForeignKey('main.Student', on_delete= models.DO_NOTHING, db_column='StudentId', blank=True, null=True, verbose_name='Student')   
    course = models.ForeignKey('main.Courses', on_delete= models.DO_NOTHING, db_column='CourseId', blank=True, null=True, verbose_name='Course')   
    applicationstageid = models.IntegerField(db_column='ApplicationStageId', blank=True, null=True, verbose_name='Application Stage')   
    remarks = models.TextField(db_column='Remarks', blank=True, null=True, verbose_name='Remarks')   
    createdby = models.CharField(db_column='CreatedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn', auto_now_add=True)   
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='ModifiedOn', auto_now=True)   
    staff= models.ForeignKey('main.Aspnetusers', blank=True, null=True,db_column='StaffId',on_delete=models.DO_NOTHING, verbose_name='Staff')
    tag= models.CharField(db_column='TagId', blank=True, null=True, verbose_name='Tag', max_length=200)
    studentreferenceno = models.CharField(db_column='StudentReferenceNo', max_length=200, blank=True, null=True, verbose_name='Student Reference No')   

    class Meta:
        managed = False
        db_table = 'Acknowledgements'
        verbose_name= 'Acknowledgement'
        verbose_name_plural= 'Acknowledgements'

    def __str__(self) -> str:
        return str(self.acknowledgementnumber)
    def __unicode__(self):
        return str(self.acknowledgementnumber)

class Aspnetroles(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=128)    
    name = models.CharField(db_column='Name', max_length=256)    
    class Meta:
        managed = False
        db_table = 'AspNetRoles'
        verbose_name='User Role'
        verbose_name_plural='User Roles'
   
    def __str__(self):
        return str(self.name)
    def __unicode__(self):
        return str(self.name)

class Aspnetuserroles(models.Model):
    userid = models.ForeignKey('main.Aspnetusers', on_delete= models.DO_NOTHING, db_column='UserId', primary_key=True, related_name="Auth_user_role", verbose_name='User')    
    roleid = models.ForeignKey('main.Aspnetroles', on_delete= models.DO_NOTHING, db_column='RoleId',verbose_name='Role')    

    class Meta:
        managed = False
        db_table = 'AspNetUserRoles'
        unique_together = (('userid', 'roleid'),)
        verbose_name='Userrole'
        verbose_name_plural='Userroles'   
    def __str__(self):
        return str(self.roleid.name)

class Aspnetusers(models.Model):
    gender_choices= (
        (0, 'Female'), 
        (1, 'Male')
        )
    id = models.CharField(primary_key=True, max_length=128, db_column='Id')
    email = models.EmailField(db_column='Email', unique=True)
    password = models.CharField(db_column='PasswordHash', blank=True, null=True, max_length=100)
    first_name = models.CharField(db_column='Name', max_length=100, unique=False, blank=True, null=True, verbose_name='Name')
    last_name = models.CharField(db_column='LastName', blank=True, null=True, max_length=128, verbose_name='Last Name')    
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True, verbose_name='Date of Birth')    
    mobile = models.CharField(db_column='Mobile', max_length=50, verbose_name='Mobile')    
    address = models.CharField(db_column='Address', blank=True, null=True, max_length=100)    
    gender= models.IntegerField(choices=gender_choices, db_column='Gender', default=1)
    company = models.CharField(db_column='Company', blank=True, null=True, max_length=100)
    countrycode = models.CharField(db_column='CountryCode', blank=True, null=True, max_length=10, verbose_name='Country Code')    
    assignedto= models.CharField(max_length=500, blank=True,null=True,help_text='ctrl+click for multiselect')  
    assignedcountries=models.CharField(max_length=100, blank=True,null=True, help_text='ctrl+click for multiselect')
    country = models.IntegerField(db_column='CountryId', blank=True, null=True, verbose_name='Country')
    state = models.IntegerField(db_column='State')    
    city = models.CharField(db_column='City', blank=True, null=True, max_length=30) 
    usertags= models.CharField(db_column='UserTags', max_length=100, blank=True, null=True)
    usertaggroups = models.CharField(db_column='UserTagGroups', blank=True, null=True, max_length=100)    
    lockenddate = models.DateTimeField(db_column='LockEndDate', blank=True, null=True, verbose_name='Lock End Date')    
    lockenabled = models.BooleanField(db_column='LockEnabled', blank=True, null=True, default=False, verbose_name='Lock Enabled')    
    isconfirmemailsent = models.BooleanField(db_column='IsConfirmEmailSent', default=False, verbose_name='Confirm Email Sent')    
    createdby = models.CharField(db_column='CreatedBy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn', auto_now_add=True)    
    updatedon = models.DateTimeField(db_column='UpdatedOn', auto_now=True)  
    photo = models.CharField(db_column='PhotoPath', blank=True, null=True, verbose_name='Photo', max_length=255)    
    #### from signalr and signalr connections table---- needto add relation
    signalrconnid = models.CharField(db_column='SignalRConnId', blank=True, null=True, max_length=128, verbose_name='SignalR Conn Id')    
    parentuser = models.EmailField(db_column='ParentUser', blank=True, null=True, max_length=100, verbose_name='Parent User')    
    notificationemails = models.TextField(db_column='NotificationEmails', blank=True, null=True, verbose_name='Notification Emails')    
    receivenotifications = models.BooleanField(db_column='ReceiveNotifications', blank=True, null=True, verbose_name='Receive Notifications')    
    emailconfirmed = models.BooleanField(db_column='EmailConfirmed', default=False, verbose_name='Email Confirmed')    
    securitystamp = models.TextField(db_column='SecurityStamp', blank=True, null=True, verbose_name='Security Stamp')    
    phonenumber = models.CharField(db_column='PhoneNumber', blank=True, null=True, max_length=12, verbose_name='Phone Number')    
    phonenumberconfirmed = models.BooleanField(db_column='PhoneNumberConfirmed', default=False, verbose_name='Phone No Confirmed')    
    twofactorenabled = models.BooleanField(db_column='TwoFactorEnabled', default=False, verbose_name='Two Factor Enabled')    
    lockoutenddateutc = models.DateTimeField(db_column='LockoutEndDateUtc', blank=True, null=True, verbose_name='Lockout End Date UTC')    
    lockoutenabled = models.BooleanField(db_column='LockoutEnabled', default=False, verbose_name='Lockout Enabled')    
    accessfailedcount = models.IntegerField(db_column='AccessFailedCount', default=0, verbose_name='Access Failed Count')    
    username = models.CharField(db_column='UserName', unique=True,max_length=256, blank=True, null=True, verbose_name='Username')    
    isshowcomssion = models.BooleanField(db_column='isShowComssion', blank=True, null=True, verbose_name='Show Commission')    
    last_login= models.DateTimeField(db_column='LastLogin', auto_now=True, blank=True,null=True)
    is_staff= models.BooleanField(db_column='IsStaff', default=False)
    is_superuser = models.BooleanField(default=False,help_text='User has all permissions',db_column='IsSuperUser')
    is_active = models.BooleanField(default=True,db_column='IsActive')
    class Meta:
        managed = False
        db_table = 'AspNetUsers'
        verbose_name='User'
        verbose_name_plural='Users'