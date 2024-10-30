import sys
import random
import argparse

from ezr import *  # import everything from ezr 

# Data lists

# Dumb vs Smart Scoring Policies
def run_dumb_strategy(N, d):
    """Run the dumb strategy and return the results."""
    dumb_results = []

   
    dumb = [guess(N, d) for _ in range(20)]  # Generate dumb strategies
    dumb_results += [d.chebyshev(lst[0]) for lst in dumb]  # Calculate Chebyshev for dumb results

    dumb_results.sort()  # Sort the dumb results
    return dumb_results

def run_smart_strategy(d):
    """Run the smart strategy and return the results."""
    smart_results = []

    
    smart = [d.shuffle().activeLearning() for _ in range(20)]  # Generate smart strategies
    smart_results += [d.chebyshev(lst[0]) for lst in smart]  # Calculate Chebyshev for smart results

    smart_results.sort()  # Sort the smart results
    return smart_results

# Updated report function to include dumb vs smart scoring
def branch_extend():
    scoring_policies = [('dumb',  run_dumb_strategy),
                        ('smart', run_smart_strategy)]
    
    print(the.train, flush=True, file=sys.stderr)
    print("\n" + the.train)
    repeats = 20
    d = DATA().adds(csv(the.train))
    b4 = [d.chebyshev(row) for row in d.rows]
    asIs, div = medianSd(b4)
    rnd = lambda z: z

    print(f"asIs\t: {asIs:.3f}")
    print(f"div\t: {div:.3f}")
    print(f"rows\t: {len(d.rows)}")
    print(f"xcols\t: {len(d.cols.x)}")
    print(f"ycols\t: {len(d.cols.y)}\n")

    somes = [stats.SOME(b4, f"asIs,{len(d.rows)}")]

    for what, how in scoring_policies:
        for the.Last in [20, 30, 40, 50]:
            start = time()
            result = []
            runs = 0
            if what == 'dumb':
                tmp_result = how(the.Last, d)
            else:  # smart strategy
                tmp_result = how(d)
            result += tmp_result
            runs += len(tmp_result)

            # Identify whether the data is low or high dimensional
            param_parts = the.train.split('/')
            sliced_train = '/'.join(param_parts[3:]) #From data/optimize/ezr , join back
           
            if len(d.cols.x) < 6 : # Atleast one xcol should be there
                dimension_category = "low_dim"
            elif len(d.cols.x) >=6:
                dimension_category = "high_dim"
            

            pre = f"{what}/dim={dimension_category}"
            tag = f"{pre},{the.Last}"
            print(tag, f": {(time() - start) / repeats:.2f} secs")
            somes += [stats.SOME(result, tag)]

    stats.report(somes, 0.01)
    # Check if it's a dataset path or 'low'/'high' option
    # if option.endswith('.csv'):
    #     data_list = [option]
    # elif option == 'low':
    #     data_list = Low_dim_data_list
    # elif option == 'high':
    #     data_list = High_dim_data_list
    # else:
    #     raise ValueError("Invalid option. Choose 'low', 'high', or a valid dataset path.")


    # for data in data_list:
    #     print(f"THE DATA {data} ----")
    #     for N in (20, 30, 40, 50):
    #         somes = []
    #         d = DATA().adds(csv(data))
    #         dumb = [guess(N, d) for _ in range(20)]
    #         dumb = [d.chebyshev(lst[0]) for lst in dumb]
    #         dumb.sort()
            
    #         the.Last = N
    #         smart = [d.shuffle().activeLearning() for _ in range(20)]
    #         smart = [d.chebyshev(lst[0]) for lst in smart]
    #         smart.sort()
    #         somes += [stats.SOME(dumb, f"dumb,{N}")]
    #         somes += [stats.SOME(smart, f"smart,{N}")]
    #         stats.report(somes)
    #     print("------")

def guess(N, d):
    some = random.choices(d.rows, k=N)
    return d.clone().adds(some).chebyshevs().rows

# Command-line argument parsing
if __name__ == "__main__":
    the.cli()
    parser = argparse.ArgumentParser(description="Process some datasets.")
    parser.add_argument('-D', action='store_true', help="An optional flag for the.Dull cohen's D")
    parser.add_argument('-t', '--dataset', type=str, help="Path to the dataset")
   
    args = parser.parse_args()

    branch_extend()