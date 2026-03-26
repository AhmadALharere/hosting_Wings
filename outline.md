# app
# لإدارة وعرض الصفحة الرئيسية
Home:
     
# model
# لتخزين وسائل التواصل لإمكانية تعديلها ديناميكياً من الداشبورد

@commit 12 : delete communication_Label models


# api:




# views:
    +home[GET]
# لعرض الصفحة الرئيسية (تم)
    +home[POST]
# عند إرسال رسالة إلى فريق الدعم من صفحة الرئيسية (تم)

    +About_us
    +FAQs
    +Baggage_info
    +Cancelation_Policy
    +Travel_Requirements
    +Refund_Policy
    +Loyalty_Program

# ملاحظة: الصفحات الأربع الدنيا يجب أن توفر كل واحدة منها روابط على الثلاث الأخرى
    +Terms_and_Conditions(Terms of Service)
    +Privecy_Policy
    +Cookie_Policy
    +Accessibility

    



# app
# لإدارة الخدمات التي يقدمها الموقع
Service:
# model:
# الخدمات لذوي الاحتياجات التي يقدمها المطار
 @commit 12: new content:
    =Special_Assistance:
        -assistence_type 
        (Wheelchair Request,Arrange assistance with boarding the aircraft,
        Arrange assistance with disembarking the aircraft,Support for the elderly or children traveling alone)
        -description
        -price
# model:
# طلبات الخدمات الخاصة عبر الانترنت
 @commit 12: new content:
    =Assestance_order:
        -user
        -special_assistance
        -Flight
        -state
        (
             pinned: تم الطلب وبانتظار الدفع
             ,ready: مت الدفع والخدمة جاهزة
             ,done: تمت الرحلة
             ,rejected: ألغيت الخدمة من طرف الشركة لعدم استيفاء الدفع
             ,canceled:ألغيت الخدمة من طرف العميل
             ,refunded: تم استرداد الأموال
              )
        -is_payed

# model:
# نموذج لحجز رحلة 
@commit 12: new content:
    =bOOKING_flight:
        -user
        -flight_type(one_direction,tow_direction)
        -flight_go
        -flight_back (null=true,blank=true for compiling with one_direction booking )
        -booking_date
        -status
            (
                PENDING: الحجز أُنشئ لكن لم يتم تأكيد الدفع بعد.
                ,CONFIRMED:الحجز تم تأكيده بنجاح بعد الدفع أو اعتماد البطاقة.
                ,CANCELLED:الحجز أُلغي من قبل العميل.
                ,REJECTED:الحجز أُلغي من قبل الشركة.
                ,COMPLETED:الرحلة أُجريت بنجاح وانتهت.
                ,EXPIRED:لم يُؤكد العميل الحجز في الوقت المحدد (مثلاً بعد 24 ساعة).
                ,REFUNDED:إذا ألغى العميل الرحلة واستعاد المبلغ.
                ,CHECKED_IN:عندما يقوم العميل بعملية الـ Check-in عبر الإنترنت أو المطار.
                ,WAITING_BACK_FLIGHT: العميل حجز رحلة ذهاب-إياب وسافر ذاهباً بالفعل, بانتظار وقت رحلة الإياب
            )
        -chears
        -chears_checked_in_go
        -chears_checked_in_back
        -chear_type ( Economy Class , Premium Economy , Business Class , First Class )
        -price
        -is_payed


# api:
    +get_booking (for current user in request)
    +booking_details (for one booking)
    +edit_booking(just edit the flight, the destination for old and new destination must be  the same{like changing travel date} , edit becoming blocked before 24h of the flight )
    +cancel_booking
    +refund_cancelling_booking
    
    +special_assistance_list
    +special_assistance_detail
    +special_assistance_ordered_list
    +special_assistance_ordered_details
    +order_special_assistance
    +cancel_special_assestince



# views:
    +Service (!?)
    +Special_Assistance
    +my_Special_asseistance
    +Book_flight
    +Manage_Booking
    +Flight_status
# من أجل البحث عن رحلة بعرفها ومعرفة وضعها وتفاصيلها

    +Check_Online
    



# app
# لإدارة صفحة وبيانات الشركة وأخبارها على الموقع
Company:
# حسابات التواصل الاجتماعي المتوفرة
    =social accounts:
       -name:charField
       -Link:charField
# model:    
# لإعلانات التوظيف في موقع الشركة
    =Careers:
        -career_name
        -description
        -positions
        -L_salary
        -U_salary
        -experience
        -published_at
# model:
# لمقالات الأخبار التي سوف يتم نشرها على لوحة الاعلانات ضمن الموقع
    =article:
        -title
        -summary
        -description
        -image_Label
        -Extra_images
        -article_type: (News,Breaking_News,Ad,discount,Notification)

# model:
# لبيانات المستثمرين
    =Investor:
        -name
        -icon
        -Bio
        -report:filefield
    
# model:
# لبيانات الشركاء الأساسيين
    =Partnerships:
        -name
        -icon
        -Description
        -business_type
        -Link

# api:

    +get_company_social_accounts


    +get_carreers_list
    +get_carreers_detail
    +submet_on_careers

    +get_articles

    +get_investor

    +get_partnerships

    


# views:
    +show_careers
    +show_careers_detail
    +Press_Room
    +News_Detail
    +Investor_Relations_page
    +Partnerships






# app
# لإدارة , إنشاء وتخزين بيانات الرحلات
Flight:


# model:
# شروط خاصة للسفر كوجود تأشيرة أو لقاح معين(كلقاح كورونا)
    =Travel_Condition:
        -name
        -description
        -icon


# model:
# مجموعة شروط جاهزة , تستخدم من أجل الدول التي تطلب مجموعة شروطط ثابتة دائماً
    =Travel_Conditions_Group:
        -name
        -description
        -Travel_conditions


# model:
# الوجهات التي تتعامل معها الشركة 
    =Destination:
        -country
        -City
        -slug
        -Bio
        -Landmarks
        -Image
        -static_rate
        -Avg_Rate
        -is_top_destination
        -Travel_cond_group_go  
        -Travel_cond_group_back


# model
# لتخزين المطارات لسهولة إعادة الاستخدامك والتأكد من صحة البيانات المدخلة
    =ِAirport:
        -name
        -Destination
        -rate
        -icon


# model:
# صف الرحلات لتخزين بيانات الرحلات المتاحة
@commit 12: new content
    =flight:
        -flight_number
        -type
        -Economy_Class_Num {Y}
        -Economy_Class_available
        -Economy_Class_price
        -Premium_Economy_Num {W}
        -Premium_Economy_available
        -Premium_Economy_price
        -Business_Class_Num {J|C}
        -Business_Class_available
        -Business_Class_price
        -First_Class_Num {F}
        -Business_Class_available
        -First_Class_price
        -counterpart
        -counterpart_airport
        -scheduled_departure
        -scheduled_arrival
        -gate
        -status


# api:

    +get_dastination_list
    +get_top_dastination

    +get_airport_list


    +get_flight_list
    +get_flight_detail

    



# views:

    +get_destinations
    +get_destination_detail
    +get_flights
    +get_flight_details
    

# app
# لإدارة المستخدمين وملفاتهم الشخصية
Accounts:
# model:
    =profile:
        -user
        -phone_number
        -image
        -Loyal_points
        -total_payment
        -total_booked

# api:
    +sign_in
    +sign_up
    +sign_up_with_google
    +sign_out
    +Profile



# views:
    +sign_in
    +sign_up
    +sign_up_with_google
    +sign_out
    +Profile

 

# app
Wings-Ai:



