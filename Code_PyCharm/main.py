from Scales.IntraLaminar import IntraLaminar


def main():

    iterations = 1000
    dt = 0.5
    layer = 5
    I_ext = 0

    intraLaminar = IntraLaminar(dt, iterations, I_ext)

    intraLaminar.run(layer)
    intraLaminar.visualize('Layer %i / %i' % (layer, layer + 1))


if __name__ == "__main__":
    main()
