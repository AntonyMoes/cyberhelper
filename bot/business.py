from random import choice

advice_group = '55836131'
# todo: register bot for obtaining this kind of shit though user api
posts = [
    '785', '2907', '2789', '2787', '2786', '2785', '2783', '2780', '2779', '2778',
    '2777', '2776', '2771', '2770', '2769', '2763', '2761', '2760', '2759', '2756',
]


async def get_advice(api) -> str:
    advice = choice(posts)

    return f'wall-{advice_group}_{advice}'

