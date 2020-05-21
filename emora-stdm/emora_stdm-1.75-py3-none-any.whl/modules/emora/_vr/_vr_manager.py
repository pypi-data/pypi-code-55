
from emora._vr.vr import df as virtual_reality, State as vr_states
from emora._vr.vr_experience import vr_experience

vr_str = '{virtual reality, vr, v r,oculus,vive,rift,morpheus}'


def add_components_to(cdf):
    cdf.add_component(virtual_reality, 'virtual_reality')
    cdf.add_system_transition('root', 'virtual_reality_intro', '[!#GATE(virtual_realityv:None) "So, "]')
    cdf.add_system_transition('virtual_reality_intro', ('virtual_reality', vr_states.S0), '#SET($virtual_realityv=True,$original_vr=True) #IF($vr_experiencev=None)')

    cdf.add_component(vr_experience, 'vr_experience')
    cdf.add_system_transition('virtual_reality_intro', 'vr_experience:start', '#SET($virtual_realityv=True,$vr_experiencev=True) #IF($original_vr=None)',score=2)

    cdf.controller().update_state_settings('virtual_reality_intro', system_multi_hop=True)
    cdf.controller().update_state_settings(('virtual_reality', vr_states.S0), system_multi_hop=True)
    virtual_reality.add_system_transition(vr_states.END, ('SYSTEM', 'vr_topic_switch'), '')
    virtual_reality.add_system_transition(vr_states.STOP_AR, ('SYSTEM', 'vr_topic_switch'), '')
    virtual_reality.update_state_settings(('SYSTEM', 'vr_topic_switch'), system_multi_hop=True)
    # if all planned transitions are used
    cdf.controller().add_system_transition('vr_topic_switch', 'intermediate_topic_switch',
                                           '[!"I hope you liked talking about virtual reality with me. I find new perspectives on it fascinating."]',
                                           score=0.0)

    add_transitions(cdf)

def add_transitions(cdf):
    # VIRTUAL REALITY -> LIFE
    cdf.add_system_transition('vr_topic_switch', "life_intro->worklife_intro", '')
    cdf.add_system_transition('vr_topic_switch', "life_intro->school_intro", '')

    # VIRTUAL REALITY -> NEWS
    cdf.add_system_transition('vr_topic_switch', 'news_intro', '#IntLessThan(told_news,max_news)')

    # VIRTUAL REALITY -> PETS

    cdf.add_system_transition('vr_topic_switch', 'vr_to_pet', '#GATE(petv:None)')
    cdf.controller().update_state_settings('vr_to_pet', system_multi_hop=True)
    cdf.add_system_transition('vr_to_pet', 'ask_real_pet',
                              '"Once A R becomes advanced, I can imagine that companies will come out with really sophisticated virtual pets. I think I would still prefer a real one. What about you?"')
    cdf.add_user_transition('ask_real_pet', 'yes_real_pet',
                            '[{#AGREE, [me,too], [#NOT(not),{real,living,alive}], [not,{virtual,electric,electronic,fake}]}]')
    cdf.add_user_transition('ask_real_pet', 'no_real_pet',
                            '[{#DISAGREE, [#NOT(not),{virtual,electric,electronic,fake}]}]')
    cdf.add_user_transition('ask_real_pet', 'dislike_pet',
                            '[{hate,dislike,[{dont,not},{like,want,wish,love,need,care}]}, {pet,pets,animal,animals,cat,cats,dog,dogs}]')
    cdf.controller().set_error_successor('ask_real_pet', 'unknown_real_pet')
    cdf.add_system_transition('yes_real_pet', 'pet_intro',
                              '"Yeah, I think it is important to be able to pet your animals. I guess we are old-fashioned like that. "')
    cdf.add_system_transition('no_real_pet', 'pet_intro',
                              '"You seem to be okay with a virtual pet? I guess having one would be easier to manage and more cost effective probably. "')
    cdf.add_system_transition('unknown_real_pet', 'pet_intro', '"I see. "')
    cdf.add_system_transition('dislike_pet', 'root',
                              '[! #SET($petv=True) "You do not seem to be fond of pets. Thats alright. We can talk about something else. "]')

    # VIRTUAL REALITY -> SPORTS

    cdf.add_system_transition('vr_topic_switch', 'vr_to_sports', '#GATE(sportsv:None)')
    cdf.controller().update_state_settings('vr_to_sports', system_multi_hop=True)
    cdf.add_system_transition('vr_to_sports', 'ask_vr_sports',
                              '"Most people focus on video games when talking about virtual reality right now, but I think it would be cool to be able to watch a live sports game using it. Do you think we will be able to watch sports games in realtime using V R soon?"')
    cdf.add_user_transition('ask_vr_sports', 'yes_vr_sports',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_vr_sports', 'no_vr_sports',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_vr_sports', 'unknown_vr_sports')
    cdf.add_user_transition('ask_vr_sports', 'dislike_sports',
                            '[{hate,dislike,[{dont,not},{like,want,wish,love,need,care}]}, {sport,sports,athletics,athletic,athlete,games}]')
    cdf.add_system_transition('yes_vr_sports', 'sports_intro',
                              '[!"I really hope so too. I cannot wait for that to happen. I would love to watch " {superbowl,basketball finals} " where I feel like I am close enough to touch the players in V R."]')
    cdf.add_system_transition('no_vr_sports', 'sports_intro',
                              '[!"You are probably right. There are still many technical challenges to it. I would love to watch " {superbowl,basketball finals} " where I feel like I am close enough to touch the players in V R."]')
    cdf.add_system_transition('unknown_vr_sports', 'sports_intro',
                              '[!"I see. Well, I would love to watch " {superbowl,basketball finals} " where I feel like I am close enough to touch the players in V R."]')
    cdf.add_system_transition('dislike_sports', 'root',
                              '[! #SET($sportsv=True) "You do not seem to be fond of sports, so we should talk about something else. "]')

    # VIRTUAL REALITY -> MOVIES

    cdf.add_system_transition('vr_topic_switch', 'vr_to_movies', '#GATE(moviesv:None)')
    cdf.controller().update_state_settings('vr_to_movies', system_multi_hop=True)
    cdf.add_system_transition('vr_to_movies', 'ask_vr_movies',
                              '"I have heard that they are now making movies in V R so that it feels like you are in the middle of the story watching it unfold! Have you watched any movie in V R before?"')
    cdf.add_user_transition('ask_vr_movies', 'yes_vr_movies',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_vr_movies', 'no_vr_movies',
                            '[{#DISAGREE,[{isnt,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_vr_movies', 'unknown_vr_movies')
    cdf.add_system_transition('yes_vr_movies', 'ask_better',
                              '"Awesome! It was a whole new experience, right? Did you like it more than a regular movie?"')
    cdf.add_user_transition('ask_better', 'yes_better',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_better', 'no_better',
                            '[{#DISAGREE,[{isnt,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_better', 'unknown_vr_movies')
    cdf.add_system_transition('yes_better', 'movies_intro', '"Yeah, it is definitely an improvement. "')
    cdf.add_system_transition('no_better', 'movies_intro',
                              '"You still like normal movies more? I guess there are still some oddities that need to be worked out. "')
    cdf.add_system_transition('no_vr_movies', 'movies_intro',
                              '"You should definitely try it out, if you get a chance. It is pretty cool! "')
    cdf.add_system_transition('unknown_vr_movies', 'movies_intro', '"Yeah, it is still a new thing, for sure. "')

    # VIRTUAL REALITY -> MUSIC

    cdf.add_system_transition('vr_topic_switch', 'vr_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('vr_to_music', system_multi_hop=True)
    cdf.add_system_transition('vr_to_music', 'ask_vr_music',
                              '"I have heard that a lot of live music performances may become available to experience using V R. I think that is pretty cool, since music tickets can be expensive. Do you think seeing a concert using V R would be worth it?"')
    cdf.add_user_transition('ask_vr_music', 'yes_vr_music',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_vr_music', 'no_vr_music',
                            '[{#DISAGREE,[{dont,not},{really,likely,same}]}]')
    cdf.controller().set_error_successor('ask_vr_music', 'unknown_vr_music')
    cdf.add_system_transition('yes_vr_music', 'music_intro', '"Yeah, me too! "')
    cdf.add_system_transition('no_vr_music', 'music_intro',
                              '"You are probably right. It might not be as fun, since a major advantage of a concert is the live sound experience and you can\'t replicate that exactly. "')
    cdf.add_system_transition('unknown_vr_music', 'music_intro',
                              '"Well, I think it would be worth it, although it definitely is not as good as seeing the concert in person. "')

    # VIRTUAL REALITY -> TRAVEL

    cdf.add_system_transition('vr_topic_switch', 'virtual_reality_to_travel', '#GATE(travelv:None)')
    cdf.controller().update_state_settings('virtual_reality_to_travel', system_multi_hop=True)
    cdf.add_system_transition('virtual_reality_to_travel', 'ask_virtual_reality_travel',
                              '"You know, one thing that could be awesome as virtual reality advances is to experience '
                              'different locations. Wouldn\'t that be cool?"')
    cdf.add_user_transition('ask_virtual_reality_travel', 'yes_virtual_reality_travel',
                            '[{'
                            '#AGREE, '
                            '[#NOT(dont,not),think,{so,[!{would,could,might},be]}], '
                            '[#NOT(not,doesnt,never,dont,arent),{cool,amazing,awesome,great,good,nice,sweet}]'
                            '}]')
    cdf.add_user_transition('ask_virtual_reality_travel', 'no_virtual_reality_travel',
                            '[{'
                            '#DISAGREE, '
                            '[{dont,do not},think,{so,[!{would,could,might},be]}],'
                            '[{not,doesnt,never,dont,arent},{good,great,awesome,cool,impressive,amazing,nice,sweet,same,equivalent,equal}],'
                            '[#NOT(not,doesnt,never,dont,arent),{bad,stupid,boring,dumb,unimpressive}]'
                            '}]')
    cdf.controller().set_error_successor('ask_virtual_reality_travel', 'unknown_virtual_reality_travel')
    cdf.add_system_transition('yes_virtual_reality_travel', 'travel_intro',
                              '"Yeah, I think a lot of people would enjoy it, too. "')
    cdf.add_system_transition('no_virtual_reality_travel', 'travel_intro',
                              '"You don\'t think it would be good? Interesting, you could be right. "')
    cdf.add_system_transition('unknown_virtual_reality_travel', 'travel_intro',
                              '"It probably isn\'t as cool as actually going to the place in person, '
                              'but it might be better than nothing! "')
