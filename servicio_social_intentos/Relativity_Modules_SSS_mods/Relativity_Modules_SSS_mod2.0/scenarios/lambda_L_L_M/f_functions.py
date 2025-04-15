from .variables import *


# def f(R):
#     return R - (lambda_staro * R_star) * (1 - (1 + (R / R_star) ** 2) ** (-beta))
# 
# def f1(R):
#     return 1 - ( (2 * lambda_staro * beta) / R_star) * (R * ((1 + (R / R_star) ** 2) ** (-beta - 1)))
# 
# def f2(R):
#     return - ((2 * lambda_staro * beta) / R_star) * (((1 + (R / R_star) ** 2) ** (-beta - 1)) * ((1 + 2 * (R / R_star) ** 2) * (-beta - 1) * ((1 + (R / R_star) ** 2) ** (-1))))
# 
# def f3(R):
#     return - ( (4 * lambda_staro * beta) / (R_star ** 3)) * (-beta - 1) * ((1 + (R / R_star) ** 2) ** (-beta - 2)) * (1 + (2 * R + 2 * ((R ** 3) / (R_star ** 2)) * (-beta - 2) * ((1 + (R / R_star) ** 2) ** (-1))))
# 
# def f32(R):
#     return f3(R) / f2(R)
# 
# # though we might need to check if we derived correctly...
# # so we'll use this other attempt


def f(R):
    return R - (lambda_staro * R_star) * (1 - (1 + (R / R_star) ** 2) ** (-beta))


def f1(R):
    """
    First derivative f'(R).
    """
    R_tilde = R / R_star
    return 1 - 2 * lambda_staro * beta * R_tilde * (1 + R_tilde ** 2) ** (-beta - 1)


def f2(R):
    """
    Second derivative f''(R).
    """
    R_tilde = R / R_star
    factor = -2 * lambda_staro * beta / R_star

    # Derivative of [R * (1 + (R/R_star)²)^(-beta - 1)] via product rule
    # We'll store the "bracket" term separately for clarity:
    bracket = (1 + R_tilde ** 2) + 2 * (-beta - 1) * R * R_tilde / R_star

    return factor * ((1 + R_tilde ** 2) ** (-beta - 2) * bracket)


def f3(R):
    """
    Third derivative f'''(R).
    """
    R_tilde = R / R_star

    # Let A(R) = (1 + R_tilde²)^(-beta - 2)
    #     B(R) = (1 + R_tilde²) + 2*(-beta - 1)*R*R_tilde/R_star
    A = (1 + R_tilde ** 2) ** (-beta - 2)
    B = (1 + R_tilde ** 2) + 2 * (-beta - 1) * R * R_tilde / R_star

    # A'(R) = derivative of (1 + R_tilde²)^(-beta - 2)
    A_prime = -2 * (beta + 2) * R_tilde / R_star * (1 + R_tilde ** 2) ** (-beta - 3)

    # B'(R) = derivative of (1 + R_tilde²) + 2*(-beta - 1)*R*R_tilde/R_star
    B_prime = -2 * (2 * beta + 1) * R / (R_star ** 2)

    # Combine via product rule
    g2 = A_prime * B + A * B_prime

    factor = -(2 * lambda_staro * beta / R_star)
    return factor * g2


def f32(R):
    return f3(R) / f2(R)
