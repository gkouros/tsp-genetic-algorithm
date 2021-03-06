""" Elimination methods for evolutionary algorithms """
import numpy as np
from selection_operators import k_tournament_selection
from fitness_utils import calc_shared_fitnesses


def fitness_sharing_elimination(
        offspring: list, population: list, lambda_: int,
        alpha: float, sigma: int) -> list:
    """ Performs the (λ+μ)-elimination with fitness sharing

    Args:
        offspring (list): List of the offspring
        population (list): List of the individuals in a population
        lambda_ (int): Number of top lambda_ candidates that will be retained

    Returns:
        new_combined: Top lambda_ candidates that are retained
    """
    # combine population and offspring
    combined = population + offspring

    # sort new population
    combined = sorted(combined, key=lambda k: k.fitness, reverse=False)

    survivors = [combined[0]]

    for _ in range(lambda_):
        fitnesses = [calc_shared_fitnesses(combined, survivors, alpha, sigma)]
        idx = np.argmin(fitnesses)
        survivors.append(combined[idx])

    return survivors


def lambda_plus_mu_elimination(
        offspring: list, population: list, lambda_: int,
        alpha: float = 1, sigma: int = 1) -> list:
    """ Performs the (λ+μ)-elimination step of the evolutionary algorithm

    Args:
        offspring (list): List of the offspring
        population (list): List of the individuals in a population
        lambda_ (int): Number of top lambda_ candidates that will be retained
        fitness_sharing (bool): Determines if the fitness_sharing is used
        alpha (float): The fitness sharing shape parameter
        sigma (int): The fitness sharing distance threshold

    Returns:
        new_combined: Top lambda_ candidates that are retained

    """
    # combine population and offspring
    combined = population + offspring

    # sort new population
    combined = sorted(combined, key=lambda k: k.fitness, reverse=False)

    # pick top lambda candidates
    combined = combined[:lambda_]

    # update fitness based on fitness sharing scheme
    if fitness_sharing:
        for idx in range(1, len(combined)):
            combined[idx].calc_shared_fitness(
                combined[:idx] + combined[idx+1:], alpha=alpha, sigma=sigma)

    return combined


def replace_worst(offspring: list, population: list, lambda_: int) -> list:
    """ Performs the (λ-μ)-elimination step of the evolutionary algorithm.

    Args:
        offspring (list): List of the offspring
        population (list): List of the individuals in a population
        lambda_ (int): Number of candidates that will be retained

    Returns:
        new_combined: The surviving candidates
    """
    combined = population[:-len(offspring)] + offspring
    new_combined = sorted(combined, key=lambda k: k.fitness, reverse=False)
    return new_combined[0:lambda_]


def k_tournament_elimination(offspring: list, population: list, lambda_: int,
                             k: int = 3) -> list:
    """ Performs elimnination with k-tournament selection

    Args:
        offspring (list): List of the offspring
        population (list): List of the individuals in a population
        lambda_ (int): Number of candidates that will be retained
        k (int): The number of participants per tournament

    Returns:
        new_combined: The surviving candidates
    """
    combined = population + offspring
    combined = sorted(combined, key=lambda k: k.fitness, reverse=False)
    new_population = [combined[0]] + \
        [k_tournament_selection(combined, k) for _ in range(lambda_-1)]
    return new_population
