LAMPORTS_PER_SOL = 1_000_000_000


def sol_to_lamports(sol: float) -> int:
    return int(sol * LAMPORTS_PER_SOL)


def lamports_to_sol(lamports: int) -> float:
    return lamports / LAMPORTS_PER_SOL
