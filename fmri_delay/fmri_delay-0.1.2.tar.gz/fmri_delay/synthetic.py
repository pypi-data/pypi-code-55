import numpy as np
from scipy import stats

def piecewise_activity(n_timepoints = 1000, trans_prob = 1e-3, trans_amp = 5, noise = 0):
    time_course = np.empty((n_timepoints))
    innovation = np.zeros_like(time_course)
    time_course[0] = np.random.normal(0, 5)
    last_trans = 0
    # Storing progression of numbers of draw (in binomial)
    n_draws = []

    t_prob = trans_prob + 0

    for t in np.arange(1, n_timepoints, 1):
        #if np.random.binomial(t - last_trans, t_prob):
        if np.random.binomial(1, t_prob):
            # Computation of transition amplitude
            transition = np.random.normal(0, trans_amp)
            
            # Store the progression of n_draws
            n_draws.extend(np.arange(t - last_trans))
            
            time_course[t] = transition
            last_trans = t
            
            # Randomization of transition probablity
            t_prob = abs(np.random.normal(trans_prob, trans_prob/4))
            
            innovation[t] = transition - time_course[t-1]
        else:
            time_course[t] = time_course[t - 1]
            
    n_draws.extend(np.arange(t - last_trans))
    
    if noise:
        time_course += np.random.normal(np.zeros_like(time_course), noise)
        innovation += np.random.normal(np.zeros_like(time_course), noise)
    
    return time_course, innovation, n_draws


def gen_follower(seed, delay, activ_prob = 100, noise = 0, rand_delay = 1):
    
    follower = np.zeros_like(seed)
    
    # Computation of random delay
    peaks = np.where(np.abs(stats.zscore(seed)) > 1.5)[0]
    shift = peaks + delay + np.random.normal(np.zeros_like(peaks), rand_delay)
    shift = np.ceil(shift).astype(int)
    
    # Discard activity at time larger than n_timepoints
    shift = shift[shift < len(seed)]
    
    # Assign a random value (from the value of the activity of the seed) to the followers
    follower[shift] = np.random.choice(seed[peaks], len(shift))
    
    # Randomly set activity of a follower to 0 with probability "activ_prob"
    n_rand_act = np.percentile(np.arange(len(shift)), 100 - activ_prob,
                               interpolation = 'nearest')
    n_rand_act = np.random.binomial(len(shift), 1 - activ_prob/100)
    rand_discard = np.random.choice(shift, n_rand_act)
    
    follower[rand_discard] = 0
    
    # Add random activity (regardless of the seed activity)
    unactiv_id = np.where(follower == 0)[0]
    rand_act = np.random.choice(unactiv_id, n_rand_act)

    follower[rand_act] = np.random.choice(seed[peaks], n_rand_act)
    
    added_noise = np.random.normal(np.zeros_like(seed), noise)
    follower += added_noise
    
    return follower

def simulate_activation(n_regions = 20, n_seeds = 0, n_followers = 0, n_second_lvl = 0,
                        n_timepoints = 400, delay = 10, activ_proba = [1e-3, 100],
                        noise = 0, **kwargs):
    # Initialization of time course
    time_course = np.empty((n_regions, n_timepoints))

    # Random group allocation of region id
    non_random_id = np.random.choice(n_regions, n_seeds + n_followers, replace = False)
    
    seeds_id = non_random_id[:n_seeds]
    followers_id = non_random_id[n_seeds:n_seeds + n_followers]
    
    # Use of innovation signals from piecewise constant voxel activity
    for i in np.arange(n_regions):
        _, time_course[i], _ = piecewise_activity(n_timepoints, activ_proba[0], noise = noise)
    
    # Generation of followers states (random choice of seed)
    seed_choice = []
    for i in range(n_followers):
        # Choice of followed seed
        if i >= n_followers - n_second_lvl:
            seed_choice.append(np.random.choice(followers_id[:(n_followers - n_second_lvl)]))
        else:
            seed_choice.append(np.random.choice(seeds_id))
        chosen = time_course[seed_choice[i]]
        # Generation of follower
        time_course[followers_id[i]] = gen_follower(chosen, delay, activ_proba[1], noise)
    
    return time_course, seeds_id, followers_id, np.array(seed_choice)