def ewma(new, prior, alpha):
    return (1-alpha)*prior + (alpha*new)