def SDD_Evaluator(SDD_Path, TSV_Path, SDD_SUMMARY):
    SDD_read = open(SDD_Path, 'r')
    f = open(TSV_Path, 'w')
    INFO_List = ['New Particle?', 'Particle Number', 'Upper X', 'Upper Y', 'Upper Z', 'Center X', 'Center Y', 'Center Z', 'Lower X',
             'Lower Y', 'Lower Z', 'Chromosome Number', 'Damage Type', 'N Direct', 'N In-direct', 'BD', 'SSB', 'DSB']
    Header = INFO_List[0]
    nn = 1
    nn_max = len(INFO_List)
    DSB = 0
    SSB = 0
    BD = 0
    Indirect = 0
    Direct = 0
    Hybrid = 0
    while nn < nn_max:
        Header = Header + '\t' + INFO_List[nn]
        nn = nn + 1
    f.write(Header + '\n')
    for line in SDD_read:
        if line[0] == '2' or line[0] == '1' or line[0] == '0':
            Export_INFO = []
            INFO = line.split(';')

            #Field 1 - Particle Specification 
            paticle_info = INFO[0].split(',')
            Exposure_INFO = paticle_info[0]
            if Exposure_INFO == '1' or Exposure_INFO == '2':
                Exposure_decision = 'Y'
            else:
                Exposure_decision = 'N'
            Export_INFO.append(Exposure_decision)
            N_part = paticle_info[1]
            Export_INFO.append(N_part)

            #Field 2 - Location Information
            Location_INFO = INFO[1].split('/')
            for Geo_INFO in Location_INFO:
                Coordiante_INFO = Geo_INFO.split(',')
                for Coordiante in Coordiante_INFO:
                    Export_INFO.append(Coordiante)

            #Field 3 - Chromosome Number Information
            Chromosome_ID = INFO[2].split(',')
            Chromosome_Number = Chromosome_ID[1]
            Export_INFO.append(Chromosome_Number)
            Chromotid_ID = Chromosome_ID[2]
            Arm_spec = Chromosome_ID[3]

            #Field 4 - Chromosome Position Information
            Chromosome_Position = INFO[3]

            #Field 5 - Cause of DNA Damage
            Cause = INFO[4].split(',')
            Damage_Specification = Cause[0]
            if Damage_Specification == '0':
                Event = 'Direct'
                Direct = Direct + 1
            if Damage_Specification == '1':
                Event = 'In-direct'
                Indirect = Indirect + 1
            if Damage_Specification == '2':
                Event = 'Hybrid'
                Hybrid = Hybrid + 1
            Export_INFO.append(Event)
            Num_Direct = Cause[1]
            Export_INFO.append(Num_Direct)
            Num_Indiret = Cause[2]
            Export_INFO.append(Num_Indiret)

            #Field 6 - Number of Damage Types
            Damage_Type = INFO[5].split(',')
            BD = BD + int(Damage_Type[0])
            SSB = SSB + int(Damage_Type[1])
            DSB = DSB + int(Damage_Type[2])
            for damage in Damage_Type:
                Export_INFO.append(damage)
            Full_break_spec = INFO[6]

            #Infomation in TSV Format
            TSV_output = Export_INFO[0]
            nnn = 1
            nnn_max = len(Export_INFO)
            while nnn < nnn_max:
                TSV_output = TSV_output + '\t' + Export_INFO[nnn]
                nnn = nnn + 1
            f.write(TSV_output + '\n')
    f.close()
    d = open(SDD_SUMMARY, 'w')
    d.write(SDD_Path + ' Evaluation'
            '\nNumber of Particle = ' + str(int(N_part) + 1) +
            '\nNumber of BD = ' + str(BD) + 
            '\nNumber of SSB = ' + str(SSB) + 
            '\nNumber of DSB = ' + str(DSB) + 
            '\nNumber of Indirect Damages = ' + str(Indirect) +
            '\nNumber of Direct Damages = ' + str(Direct) +
            '\nNumber of Hybrid Damages = ' + str(Hybrid)
           )
    d.close()