

def reachedSteadtStateAtDay(
    aggData,
    safety=.01,
    finalFrame=-1
):
    """
    Description:
        * Calculates the point at which the aggregated alleles reach their
            steady state (defined by the final frame of the simulation).
    In:
        * aggData: Genotypes aggregated data.
        * safety: Envelope of values around the steady state that are
            considered "stable" (as a proportion of the final total allele
            composition).
        * finalFrame: Index of the day to be considered as "stable" for
            reference purposes.
    Out:
        * steadtStateReach: Day at which the dynamics of the system became
            stable.
    Notes:
        * This is a quick and simple way to calculate the steady state, but
            assumes that the system stabilizes and that the simulation was
            run for enough time for the dynamics to become stable.
    """
    finalFrame = aggData["population"][finalFrame]
    tolerance = round(sum(finalFrame) * safety)
    toleranceUp = finalFrame + tolerance
    toleranceDown = finalFrame - tolerance

    daysMax = len(aggData["population"])

    for i in range(0, daysMax):
        steadyStateReach = daysMax
        testFrame = aggData["population"][i]

        boolsUp = testFrame < toleranceUp
        boolsDown = testFrame > toleranceDown

        if all(boolsUp) and all(boolsDown):
            steadyStateReach = i
            break

    return steadyStateReach
