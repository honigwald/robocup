def dance():

    names = []
    times = []
    keys = []

    # Keyframes
    names.append("LShoulderPitch")
    times.append([1.8, 5.7, 7.7, 11.7, 13.7])
    keys.append([1.0436, 2.0857, 1.0436, 2.0857, 1.0436])

    names.append("LShoulderRoll")
    times.append([2, 3, 4 , 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    keys.append([1.3265, -0.3142, 1.3265, -0.3142, 1.3265, -0.3142, 1.3265, -0.3142, 1.3265, -0.3142,  1.3265, -0.3142, 1.3265, -0.3142])

    names.append("RShoulderPitch")
    times.append([1.7000, 3.7000, 7.7000, 9.7, 13.7])
    keys.append([2.0857, 1.0436, 2.0857, 1.0436, 2.0857])

    names.append("RShoulderRoll")
    times.append([0.3 ,2, 3, 4 , 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    keys.append([-1.3265, 0.3142, -1.3265, 0.3142, -1.3265, 0.3142, -1.3265, 0.3142, -1.3265, 0.3142, -1.3265, 0.3142, -1.3265, 0.3142, -1.3265])

    return names, times, keys
