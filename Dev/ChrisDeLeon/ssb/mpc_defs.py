import detector

def experiment(name, kernel, location, c, *args, **kwargs):
    return name, c, detector.Detector(kernel, 
                                      location, 
                                      n_clusters=c, 
                                      *args, 
                                      **kwargs).run()
