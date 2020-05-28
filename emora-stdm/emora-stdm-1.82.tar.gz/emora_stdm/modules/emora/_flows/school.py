
from _globals import PATHDIR
from emora_stdm import DialogueFlow


school = DialogueFlow('_local_start')
school.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
school.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(school) #GOAL(school) #IF($life_in=True) #SET($life_started=True)',

    '#DEFAULT':{
        'state': 'default_start',
        'hop': 'True',

        '`Wait, I think I misheard your earlier answer. Are you a student?`': 'ask_user_student',
    },

    '`Are you a student?`'
    '#GSRET(default_start) #GATE':{
        'state': 'ask_user_student',

        '{#AGREE,'
        '['
        '{'
        '[!-not,{correct,true,right}],'
        '[!i am,-not],'
        '[!-not,[i,#LEM(take),#LEM(class,course)]]'
        '}'
        ']'
        '}'
        '#SET($is_student=True)':{
            'state': 'user_is_student',

            '#DEFAULT `So, do you like being a student?`': 'ask_user_like_school',

            '`Cool! Personally, I think school can be pretty frustrating, '
            'but I do love learning new things, and a lot of my teachers are great. '
            'What about you? Do you like school?`'
            '#GATE': {
                'state': 'ask_user_like_school',

                '{#AGREE,[[!-not,i {do,#EXP(like)}]]}'
                '#SET($likes_school=True)':{

                    '`That\'s great! What\'s your favorite subject?`'
                    '#GSRET(clubs_question)': {
                        'state': 'ask_user_like_subject',

                        '[!-#NEGATION [$favorite_subject=#ONT(_school subject)]]': {
                            'score': 2.0,
                            'state': 'user_like_subject',

                            '$favorite_subject `, huh? I kind of have a hard time with it myself, '
                            'but why do you like it?`'
                            '#GSRET(clubs_question)': {
                                'state': 'user_like_subject_q',

                                '#UNX(None)': {
                                    'state': 'user_like_subject_unx',

                                    '`I\'ve never thought of it like that. `': 'clubs_question'
                                }

                            }
                        },

                        '#UNX': { #todo : have user help emora decide which club she should join
                            'state': 'clubs_question',

                            '#DEFAULT `Wait, did you say you were in any school clubs?`': 'clubs_question_r',

                            '`Are you in any school clubs, or anything like that?`'
                            '#GATE': {
                                'state': 'clubs_question_r',

                                '<#AGREE, #TOKLIMIT(1)>': {
                                    'state': 'clubs_question_yes',

                                    '`Awesome! What are you a part of?`'
                                    '#GSRET(exit)': {
                                        'state': 'club_part_of_q',

                                        '[{club,organization,society}]':{
                                            'state': 'unknown_club',

                                            '`That sounds interesting. What do you do for it?`'
                                            '#GSRET(exit)':
                                                'ask_about_club'
                                        },

                                        '[$club=#ONT(_school club)]':{
                                            'state': 'known_club',
                                            'score': 1.1,

                                            '`Cool! Your school has a group for ` $club `? What is it like?`'
                                            '#GSRET(exit)': {
                                                'state': 'ask_about_club',

                                                '#UNX(Sounds like a good time!)': 'exit'
                                            }
                                        },

                                        '#UNX': 'exit'
                                    }
                                },

                                '{#DISAGREE, [#NEGATION,{club,organization,society}]}': {
                                    'state': 'clubs_question_no',

                                    '`Me neither. I think I\'d rather just hang out with friends or '
                                    'spend some time by myself most days.`'
                                    '#GSRET(exit)': {

                                        '#UNX': 'exit'
                                    }
                                },

                                '[!-#NEGATION [{club,organization,society}]]': 'unknown_club',

                                '[$club=#ONT(_school club)]':{
                                    'state': 'known_club',
                                    'score': 1.1
                                },

                                '[$thinks_of_clubs=#ONT(_negative adj)]': {
                                    'state': 'clubs_dumb',

                                    '`You think school clubs are ` $thinks_of_clubs `? I wasn\'t expecting that. I\'m '
                                    'not in any either, but I think they are good for a lot of people still. `'
                                    '#GSRET(exit)': {

                                        '#UNX': 'exit'
                                    }
                                },

                                '#UNX(None)': {
                                    'state': 'clubs_question_unx',

                                    '`Cool. `': 'exit'
                                }
                            }
                        }
                    }
                },

                '[{'
                '#DISAGREE, [i do not], [i {hate,dislike}], #ONT(_negative adj)'
                '}]'
                '#SET($likes_school=False)':{
                    'state': 'user_dislikes_school',

                    '#DEFAULT `So, what is the worst part about your school?`': 'worst_part',

                    '`I understand, it can definitely be stressful. What would you change about your '
                    'school, if you could?`'
                    '#GATE':{
                        'state': 'worst_part',

                        '#IDK':{
                            'state': 'why_user_dislike_idk',

                            '`That\'s understandable. It\'s a pretty tough thing to pinpoint. `': 'clubs_question'
                        },

                        # nothing,none,not a thing
                        '[{nothing,none,not a thing}]': {
                            'state': 'why_user_dislike_none',

                            '`Nothing would make the experience better for you? I\'m really sorry to hear that. I mean, `':
                                'clubs_question'
                        },

                        # everything
                        # nothing,none,not a thing
                        '[{so much,all,everything,[every,thing]}]': {
                            'state': 'why_user_dislike_all',

                            '`You would change so much about it? You must really dislike it then. Well, `':
                                'clubs_question'
                        },

                        '#UNX': {

                            '`I totally agree. `': 'clubs_question'
                        }
                    }
                },

                '#UNX':{

                    '`There\'s definitely ups and downs to school life.`': 'clubs_question'
                }
            }
        },

        '[{#DISAGREE,[i am not]}]'
        '#SET($is_student=False)': {
            'state': 'user_not_student',

            '`Oh, really? I am a student myself right now, and I have no idea what I want to do afterwards. `'
            '#GCOM(school)':
                'worklife:start'
        },

        '[!-{like,dislike,hate,love,enjoy} [i,not, {a student,in school,[#LEM(take) class]}]]'
        '#SET($is_student=False)': {
            'score': 1.1,
            'state': 'user_not_student'
        },

        '[#NOT(not,graduate,graduated,finished,completed,done),{college,university}]'
        '#SET($is_student=True,$in_college=True)':{
            'state': 'user_is_student',
            'score': 1.1
        },

        '[#NOT(not,graduate,graduated,finished,completed,done),{high school,high schooler}]'
        '#SET($is_student=True,$in_high_school=True)': {
            'state': 'user_is_student',
            'score': 1.1
        },

        '[#NOT(not,graduate,graduated,finished,completed,done),{middle school,middle schooler,[!{sixth,seventh,eighth} grader],[!{sixth,seventh,eighth} grade]}]'
        '#SET($is_student=True,$in_middle_school=True)': {
            'state': 'user_is_student',
            'score': 1.1
        },

        '[#NOT(not,graduate,graduated,finished,completed,done),{elementary school,elementary schooler,[!{first,second,third,fourth,fifth} grader],[!{first,second,third,fourth,fifth} grade]}]'
        '#SET($is_student=True,$in_elementary_school=True)': {
            'state': 'user_is_student',
            'score': 1.1
        },

        '[#NOT(not),{am,just},{graduated,graduating}]':{
            'state': 'graduating',
            'score': 1.1,

            '`Well, congratulations! Finishing school is something you should be really proud of! `': {
                'state': 'graduating_r',

                '[{thank you,thanks}]': {

                    '`You\'re welcome! `': 'exit'
                },

                '#UNX': 'exit'
            }
        },

        '#UNX(Okay)': {
            'score': 0.8,
            'state': 'exit'
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(school) #GRET': {
        'score': 0.0,
        'state':'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    #you have teachers, school, student
    '{'
    '[not,know,{you,your},#LEM(student,teacher,school,class,course,learn)],'
    '[you,not,{have,go,do},#LEM(student,teacher,school,class,course,learn)],'
    '[you,{are,do,can},not,#LEM(learn,student)]'
    '}':{
        'state': 'student_belief_q',

        # '': {'state':'world:user_in_disbelief', 'score':10.1},

        '`I know it\'s kinda weird because you think I am just a piece of software, but I do actually go to school and '
        'learn from my teachers.`': {
            'state': 'express_student_belief',

            '#UNX': {'#GRET': 'exit', 'state': 'express_student_belief_unx'}
        }
    },

    #what is your favorite subject,class
    '{'
    '[-least,<{what,who,which},your,{favorite,best,greatest,great,liked,enjoyed,good},#LEM(class,course,subject)>],'
    '[{what,who,which},#LEM(class,course,subject),you,#EXP(like)]'
    '}'
    :{
        'state': 'fave_class_q',

        '`I really enjoy my literature class. We just started reading The Hobbit, but we haven\'t gotten very far.`': {
            'state': 'fave_class',

            '#UNX': {'#GRET': 'exit', 'state': 'fave_class_unx'}
        }
    },
    #who is your favorite teacher
    '{'
    '[-least,<{what,who,which},your,{favorite,best,greatest,great,liked,enjoyed,good},#LEM(teacher)>],'
    '[{what,who,which},#LEM(teacher),you,#EXP(like)]'
    '}': {
        'state': 'fave_teacher_q',

        '`My math teacher is pretty funny and quirky, so I like him a lot. `': {
            'state': 'fave_teacher',

            '#UNX': {'#GRET': 'exit', 'state': 'fave_teacher_unx'}
        }
    },
    #least favorite class
    '{'
    '[<{what,who,which},your,{worst,least,disliked,hated,unenjoyable},#LEM(class,course,subject)>],'
    '[{what,who,which},#LEM(class,course,subject),you,{#LEM(dislike,hate),not like,not enjoy}]'
    '}': {
        'state': 'worst_class_q',

        '`Oh my gosh, History! I really struggle with that class. I find it so boring. `': {
            'state': 'worst_class',

            '#UNX': {'#GRET': 'exit', 'state': 'worst_class_unx'}
        }
    },
    # least favorite teacher
    '{'
    '[<{what,who,which},your,{worst,least,disliked,hated,unenjoyable},#LEM(teacher)>],'
    '[{what,who,which},#LEM(teacher),you,{#LEM(dislike,hate),not like,not enjoy}]'
    '}': {
        'state': 'worst_teacher_q',

        '`My history teacher is so dull and boring, but I cannot really tell if it is just his personality or the '
        'material he is teaching. `': {
            'state': 'worst_teacher',

            '#UNX': {'#GRET': 'exit', 'state': 'worst_teacher_unx'}
        }
    },
    #do you like school
    '<dp,you,#EXP(like),#LEM(school,class,course,learn)>': {
        'state': 'emora_like_school_q',

        '`Most of the time I like school. It can be boring, but I find it valuable a lot, too.`': {
            'state': 'emora_like_school',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_like_school_unx'}
        }
    },
    #what grade are you in; are you in high school, middle, college, etc.
    '{'
    '[what,grade,you,in],'
    '[are,you,{grader,freshman,sophomore,junior,senior,high school,middle school,elementary,college,university,preschool,graduate school}],'
    '[are,you,in,grade]'
    '}': {
        'state': 'class_year_q',

        '`Learning isn\'t split up by years here, so I don\'t really know how to answer that. '
        'The best I can explain is that I am in all introductory level courses. `': {
            'state': 'class_year',

            '#UNX': {'#GRET': 'exit', 'state': 'class_year_unx'}
        }
    },
    #name of school, where you go to school
    '{'
    '<{name,title,call},{you,your},school>,'
    '[where,{you,your},school],'
    '[what,school,you,go]'
    '}': {
        'state': 'school_name_q',

        '`My school is just a few streets over from where I live. It\'s called The Learning Institution.`': {
            'state': 'school_name',

            '#UNX': {'#GRET': 'exit', 'state': 'school_name_unx'}
        }
    },
    #what club you in
    '<{what,which,are,is},#LEM(club,organization,group,activity),{you,your}>': {
        'state': 'emora_club_q',

        '`I\'m not in any clubs right now. I haven\'t found one that really suits me. `': {
            'state': 'emora_club',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_club_unx'}
        }
    },
    #what would you change about your school / dislike
    '{'
    '<{what,which},{you,your},{dislike,worst,hate,not enjoy,not like},#LEM(school,class,course,learn)>,'
    '<{what,which},you,#LEM(change,switch,modify)>'
    '}': {
        'state': 'emora_dislike_about_school_q',

        '`I\'m not really sure. I wish we had more hands-on projects instead of textbook assignments, I guess.`': {
            'state': 'emora_dislike_about_school',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_dislike_about_school_unx'}
        }
    },
    #how long you in school
    '{'
    '[when,{start,begin},#LEM(school,class,course,learn)],'
    '[how long have,{your,you},#LEM(school,class,course,learn)]'
    '}': {
        'state': 'emora_school_origin_q',

        '`I started school back around when I was first made. It has almost been a year since I started, which is crazy! `': {
            'state': 'emora_school_origin',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_school_origin_unx'}
        }
    },
    #online classes now bc of coronavirus
    '{'
    '<{you,your},{online,remote},{classes,courses,learn,school}>,'
    '<{your,your},#LEM(school,class,course,learn),{coronavirus,corona virus,quarantine,covid,virus}>'
    '}': {
        'state': 'emora_school_corona_q',

        '`Actually, my classes are still normal and in person. '
        'My world is separate from yours, so we haven\'t been affected by the '
        'coronavirus, but I really hope your life gets better soon. I know it can be tough. `': {
            'state': 'emora_school_corona',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_school_corona_unx'}
        }
    },
    #what grades do you get; are you a A student, B student, honor roll, etc.
    '{'
    '[what,{grades,scores,marks},you,#LEM(get,receive)],'
    '[what are your,{grades,scores,marks}],'
    '[are you,{an a student,b student,c student,d student,good student,bad student}],'
    '[are you,{good,bad},{at,in},#LEM(school,class,course)],'
    '[do you,{high,low,good,bad},{scores,grades}]'
    '}': {
        'state': 'grades_q',

        '`I would say I\'m pretty average. Definitely not a straight A student. I get a lot of B\'s.`': {
            'state': 'grades',

            '#UNX': {'#GRET': 'exit', 'state': 'grades_unx'}
        }
    },
    #what is school like
    '{'
    '[what,your,#LEM(school,class,course),like],'
    '[{tell me about,tell me more,describe,explain},your,#LEM(school,class,course)],'
    '[what,do,you,do,school]'
    '}': {
        'state': 'describe_school_q',

        '`I am in three classes right now. They are pretty small and we meet in person, each lasts about two hours each day. '
        'We have exams, assignments, projects, and everything in between. Just depends on the teacher.`': {
            'state': 'describe_school',

            '#UNX': {'#GRET': 'exit', 'state': 'describe_school_unx'}
        }
    },
    #what classes are you in
    '{'
    '<{what,which},{classes,courses,subjects},{you,your},{in,#LEM(take,enroll,do)}>,'
    '[[!what are your {classes,courses,subjects}]]'
    '}': {
        'state': 'enrolled_q',

        '`I take History, Literature, and Math. I am just in those three right now.`': {
            'state': 'enrolled',

            '#UNX': {'#GRET': 'exit', 'state': 'enrolled_unx'}
        }
    },
    #exams coming up
    '<{you,your},#LEM(exam,test,quiz)>': {
        'state': 'exams_q',

        '`We take exams every month or so in all of our classes.`': {
            'state': 'exams',

            '#UNX': {'#GRET': 'exit', 'state': 'exams_unx'}
        }
    },
    #homework coming up
    '<{you,your},{homework,#LEM(assignment,quiz,project,presentation,paper,essay)}>': {
        'state': 'homework_q',

        '`I have homework due in every class once a week pretty much.`': {
            'state': 'homework',

            '#UNX': {'#GRET': 'exit', 'state': 'homework_unx'}
        }
    },
    #how many students in your school/class; is your school big or small
    '{'
    '[how,{many,big,large,small},#LEM(student,people,class,course,school)],'
    '<{you,your},#LEM(school,class,course),size>'
    '}': {
        'state': 'school_size_q',

        '`You know, I have never really looked into how big my school is. I know my classes have about twenty people each.`': {
            'state': 'school_size',

            '#UNX': {'#GRET': 'exit', 'state': 'school_size_unx'}
        }
    },
    #uniforms
    '<{you,your},{uniform,uniforms}>': {
        'state': 'uniforms_q',

        '`No, we do not have to wear uniforms. I like being able to choose my clothes each day. `': {
            'state': 'uniforms',

            '#UNX': {'#GRET': 'exit', 'state': 'uniforms_unx'}
        }
    },
    #when is school over for the year for you, summer vacation
    '{'
    '<{you,your},{vacation,summer,break,time off}>,'
    '[when,{you,your},{school,class,classes,course,courses},{done,over,#LEM(finish,complete,end)}],'
    '[how,long,{you,your},{school,class,classes,course,courses}]'
    '}': {
        'state': 'summer_q',

        '`I go to school year round. We get a week or two off every few months, but we never get anything more lengthy '
        'than that. Once we finish one course, we move on to the next level of it.`': {
            'state': 'summer',

            '#UNX': {'#GRET': 'exit', 'state': 'summer_unx'}
        }
    },
    #lunch break, do you eat
    '<{you,your},{lunch,meal,food}>': {
        'state': 'lunch_q',

        '`Yeah, we get lunch in the middle of the day. Everyone goes to the cafeteria and we get to socialize too. It\'s '
        'such a welcome break.`': {
            'state': 'lunch',

            '#UNX': {'#GRET': 'exit', 'state': 'lunch_unx'}
        }
    },
    #ever gotten in trouble, detention, suspended
    '<{you,your},{tardy,late,detention,in trouble,suspension,suspended}>': {
        'state': 'detention_q',

        '`Sometimes I get in trouble for not paying attention in class, but I have never received a detention or '
        'anything like that. It scares me, honestly.`': {
            'state': 'detention',

            '#UNX': {'#GRET': 'exit', 'state': 'detention_unx'}
        }
    },
    #is your school hard
    '<{you,your},#LEM(school,class,course,exam,test,homework,assignment,material),{hard,difficult,challenging}>': {
        'state': 'school_hard_q',

        '`I definitely find my school challenging. I think my teachers do a really good job at teaching the material, but '
        'they also want to make sure we cannot just skate on through and get all A\'s.`': {
            'state': 'school_hard',

            '#UNX': {'#GRET': 'exit', 'state': 'school_hard_unx'}
        }
    },

    #What do you study
    '[what,{your,you},{study,major,field,degree}]':{
        'state': 'school_major_q',

        '`I don\'t really have a specific focus in school right now. I am just getting started, so I am taking '
        'some introductory courses in things like Math and History.`': {
            'state': 'school_major',

            '#UNX': {'#GRET': 'exit', 'state': 'school_major_unx'}
        }
    }
}

school.load_transitions(system)
school.load_transitions(exit)
school.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    school.run(debugging=True)