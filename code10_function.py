
def job_j(user,path_input,path_output):
    from sqlalchemy import create_engine, types
    import pandas as pd
    import time
    from datetime import datetime

    t_preliminary_0 = time.time()
    # Set user.
    #user='A30004560'
    # Create engine.
    engine = create_engine('hana://{user}@hananode1:30015'.format(user=user))
    
    #path_input = "P:/New Energy/Churn Moveout Report/Input_file/Full VPPSA Site List V3.xlsx"
    df1 =pd.read_excel(path_input)
    
    df1.to_sql('vpp_churn_tom_from_python', engine, schema=user, if_exists='replace', dtype=types.NVARCHAR(length=255))
    
    t_preliminary_1 =  time.time()
    
    # Wait for 5 seconds
    #time.sleep(300)
    
    t_sql_code_0 = time.time()
    sql="""
    SELECT A."Inverter", A."POD (NMI)" NMI, A."*approved BP*" BP_VPP, C.BUSINESSPARTNER BP_Active,C.COMPANY,
    min(CASE WHEN C.BUSINESSPARTNER IS NULL THEN '3_LeftVPP_New_NonAGL_Customer' 
    WHEN C.BUSINESSPARTNER IS NOT NULL AND right(A."*approved BP*",9) <> right(C.BUSINESSPARTNER,9) and C.COMPANY != 'AGL' THEN '3_LeftVPP_New_NonAGL_Customer'
    WHEN C.BUSINESSPARTNER IS NOT NULL AND right(A."*approved BP*",9) <> right(C.BUSINESSPARTNER,9) THEN '4_LeftVPP_New_AGL_Customer'
    when C.BUSINESSPARTNER IS NOT NULL AND right(A."*approved BP*",9) = right(C.BUSINESSPARTNER,9) and C.COMPANY = 'PD' THEN '2_PowerDirect'
    ELSE '1_CURRENT' END) AS STATUS
    , CASE WHEN A."*approved BP*" IS NOT NULL THEN (SELECT max(MOVEINDATE) from "SP_CUSTOMER"."CIA_TheTruthAboutCustomer"D where right(D.BUSINESSPARTNER,9) = right(A."*approved BP*",9) and left(D.NMI,10)=left(A."POD (NMI)",10)) END VPP_MOVEIN
    , CASE WHEN A."*approved BP*" IS NOT NULL THEN (SELECT max(MOVEOUTDATE) from "SP_CUSTOMER"."CIA_TheTruthAboutCustomer"D where right(D.BUSINESSPARTNER,9) = right(A."*approved BP*",9) and left(D.NMI,10)=left(A."POD (NMI)",10)) END VPP_MOVEOUT
    ,CASE WHEN C.BUSINESSPARTNER IS NOT NULL THEN (SELECT max(MOVEINDATE) from "SP_CUSTOMER"."CIA_TheTruthAboutCustomer"D where right(D.BUSINESSPARTNER,9) = right(C.BUSINESSPARTNER,9)and left(D.NMI,10)=left(C.NMI,10)) END CURRENT_CUSTOMER_MOVEIN
    
    from
    	(SELECT * from "{user}"."VPP_CHURN_TOM_FROM_PYTHON") A
    
    left join
    
    	(SELECT * FROM "SP_CUSTOMER"."CIA_TheTruthAboutCustomer" B
    	WHERE FUEL = 'ELEC' AND STATUS = 'ACTIVE'
    	) C on left(A."POD (NMI)",10) = left(C.NMI,10)
    
    GROUP BY A."Inverter", A."POD (NMI)", A."*approved BP*", C.NMI, C.BUSINESSPARTNER, C.TYPE, C.STATE, C.STATUS, C.COMPANY
    order by STATUS
        """.format(user=user)
    
    df2 = pd.read_sql(sql, engine)
    t_sql_code_1 = time.time()
    
    t_exportfile_code_0 = time.time()
    #today = datetime.today().date()  
    
    #path_output = "P:/New Energy/Churn Moveout Report/Full VPPSA Site List V4 outputfile {datetime}.xlsx" .format(datetime=today)
      
    df2.to_excel(path_output)
    t_exportfile_code_1 = time.time()
    
    category_all= df2['nmi'].nunique()
    category_1 = df2.groupby('status')['nmi'].nunique()['1_CURRENT']
    category_2 = df2.groupby('status')['nmi'].nunique()['2_PowerDirect']
    category_3 = df2.groupby('status')['nmi'].nunique()['3_LeftVPP_New_NonAGL_Customer']
    category_4 = df2.groupby('status')['nmi'].nunique()['4_LeftVPP_New_AGL_Customer']
    
    ##log
    f= open("P:/New Energy/Churn Moveout Report/LOG_RUN.txt", "a+")
    f.write("%s, %s, %s, %s, %s\n"%(time.strftime("%x, %X"), len(df2), t_preliminary_1-t_preliminary_0,t_sql_code_1-t_sql_code_0,t_exportfile_code_1-t_exportfile_code_0))
    f.close()
    return