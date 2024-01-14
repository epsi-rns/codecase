import uno

def get_desktop() \
      -> 'com.sun.star.frame.XDesktop':

    'com.sun.star.uno.XComponentContext'
    local_context = uno.getComponentContext()

    'com.sun.star.bridge.UnoUrlResolver'
    resolver = local_context.ServiceManager. \
      createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver",
        local_context)

    'com.sun.star.uno.XComponentContext'
    context = resolver.resolve(
      "uno:socket,host=localhost,port=2002;"
      + "urp;StarOffice.ComponentContext")

    'com.sun.star.frame.XDesktop'
    desktop = context.ServiceManager. \
      createInstanceWithContext(
        "com.sun.star.frame.Desktop", context)
    
    return desktop

def create_calc_instance(
      desktop: 'com.sun.star.frame.XDesktop') \
      -> 'com.sun.star.frame.XModel':

    document = desktop.loadComponentFromURL(
      "private:factory/scalc", "_blank", 0, ())

    return document

if __name__ == "__main__":
    desktop  = get_desktop()
    document = create_calc_instance(desktop)

