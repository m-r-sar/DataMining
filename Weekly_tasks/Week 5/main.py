import numpy as np
import pandas as pd
import scipy


def tcriteria(x, y, a=0.05, equal_var=True, alternative='two-sided'):
    len_x = len(x)
    len_y = len(y)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_std = np.std(x, ddof=1)
    y_std = np.std(y, ddof=1)

    if equal_var:
        df = len_x + len_y - 2
        sp = np.sqrt(((len_x - 1) * x_std ** 2 + (len_y - 1) * y_std ** 2) / df)
        se_total = sp * np.sqrt(1 / len_x + 1 / len_y)
        t = (x_mean - y_mean) / se_total
    else:
        se2_x = (x_std ** 2) / len_x
        se2_y = (y_std ** 2) / len_y
        se_total = np.sqrt(se2_x + se2_y)
        df = (se2_x + se2_y) ** 2 / ((se2_x ** 2 / (len_x - 1)) + (se2_y ** 2 / (len_y - 1)))

        t = (x_mean - y_mean) / se_total

    critical_value = scipy.stats.t.ppf(1-a/2, df)

    down_border = (x_mean - y_mean) - critical_value*se_total
    top_border = (x_mean - y_mean) + critical_value*se_total

    if alternative == 'two-sided':
        p_value = 2 * scipy.stats.t.sf(np.abs(t), df)
    elif alternative == "one-sided-greater":
        p_value = scipy.stats.t.sf(t, df)
    elif alternative == "one-sided-less":
        p_value = scipy.stats.t.cdf(t, df)
    else:
        p_value = None

    return {"t_stat": t, "p_value": p_value, "df": df, "borders": (down_border, top_border)}

def ucriteria(x, y):
    len_x = len(x)
    len_y = len(y)
    N = len_x+len_y

    a = np.concatenate([x, y], axis=0)

    rank = a.argsort().argsort() + 1

    unique, inverse = np.unique(a, return_inverse = True)

    unique_rank_sum = np.zeros_like(unique)
    np.add.at(unique_rank_sum, inverse, rank)
    unique_count = np.zeros_like(unique)
    np.add.at(unique_count, inverse, 1)

    unique_rank_mean = unique_rank_sum.astype(float) / unique_count

    rank_mean = unique_rank_mean[inverse]

    x = rank_mean[:len_x]
    y = rank_mean[len_x:]

    U = np.sum(x) - (len_x*(len_x+1)/2)

    unique_ranks, counts = np.unique(rank_mean, return_counts=True)
    tie_sum = np.sum(counts**3 - counts)
    var_base = (len_x*len_y) / (N*(N-1))
    var_adjustment = ((N**3 - N) - tie_sum) / 12
    sigma_corr = np.sqrt(var_base * var_adjustment)

    mu_u = (len_x*len_y) / 2
    z = (np.abs(U - mu_u) - 0.5) / sigma_corr
    p_val = 2 * scipy.stats.norm.sf(z)

    return {"U_value": U, "p_value": p_val}


if __name__ == '__main__':
    rng = np.random.default_rng(seed=42)

    datasets = {
        "Normal (μ=0, σ=10)": (rng.normal(0, 10, 1000), rng.normal(0, 10, 1000)),
        "Normal (μ=100, σ=1)": (rng.normal(100, 1, 100), rng.normal(100, 1, 100)),
        "Exponential (λ=2)": (rng.exponential(2, 1000), rng.exponential(2, 1000))
    }

    results = []

    for name, (x, y) in datasets.items():
        custom_t = tcriteria(x, y)
        scipy_t = scipy.stats.ttest_ind(x, y)

        results.append({
            "Dataset": name,
            "Test": "T-Test",
            "Custom Stat": custom_t['t_stat'],
            "SciPy Stat": scipy_t.statistic,
            "Custom p-value": custom_t['p_value'],
            "SciPy p-value": scipy_t.pvalue,
            "Stat Diff": abs(custom_t['t_stat'] - scipy_t.statistic),
            "p-value Diff": abs(custom_t['p_value'] - scipy_t.pvalue)
        })

        custom_u = ucriteria(x, y)
        scipy_u = scipy.stats.mannwhitneyu(x, y)

        custom_u_stat = custom_u['U_value']

        results.append({
            "Dataset": name,
            "Test": "Mann-Whitney U",
            "Custom Stat": custom_u_stat,
            "SciPy Stat": scipy_u.statistic,
            "Custom p-value": custom_u['p_value'],
            "SciPy p-value": scipy_u.pvalue,
            "Stat Diff": abs(custom_u_stat - scipy_u.statistic),
            "p-value Diff": abs(custom_u['p_value'] - scipy_u.pvalue)
        })

    df = pd.DataFrame(results)
    pd.options.display.float_format = '{:.4e}'.format
    print("\n--- Statistical Implementation Comparison ---")
    print(df.to_string(index=False))