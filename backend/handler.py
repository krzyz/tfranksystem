from trueskill import Rating, rate, expose

def main(event, context):
    alice, bob, eve, trudy = Rating(), Rating(), Rating(), Rating()  # assign Alice and Bob's ratings
    print(f'{alice=}, {bob=}, {eve=}, {trudy=}')
    [(alice,), (bob,), (eve,), (trudy,)] = rate([(alice,), (bob,), (eve,), (trudy,)], ranks=[0,1,2,3])
    print(f'{alice=}, {bob=}, {eve=}, {trudy=}')
    leaderboard = sorted([alice, bob, eve, trudy], key=expose, reverse=True)
    print(f'{leaderboard=}')

if __name__ == "__main__":
    main('', '')