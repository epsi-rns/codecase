import uno

def get_desktop() \
      -> 'com.sun.star.frame.XDesktop':

    'com.sun.star.uno.XComponentContext'
    local_context = uno.getComponentContext()

    'com.sun.star.uno.XInterface'
    resolver = local_context.ServiceManager. \
      createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver",
        local_context)

    # 'com.sun.star.uno.XInterface'
    context = resolver.resolve(
      "uno:socket,host=localhost,port=2002;"
      + "urp;StarOffice.ComponentContext")

    # 'com.sun.star.frame.XDesktop'
    desktop = context.ServiceManager. \
      createInstanceWithContext(
        "com.sun.star.frame.Desktop", context)
    
    return desktop

def create_calc_instance(
      desktop: 'com.sun.star.frame.XDesktop') \
      -> 'com.sun.star.sheet.SpreadsheetDocument':

    document = desktop.loadComponentFromURL(
      "private:factory/scalc", "_blank", 0, ())

    return document

def open_document(
      desktop: 'com.sun.star.frame.XDesktop',
      file_path: str) -> 'com.sun.star.sheet.SpreadsheetDocument':

    document = desktop.loadComponentFromURL(
      f"file://{file_path}", "_blank", 0, ())

    return document

def get_file_path(filename: str) -> str:
  import os

  script_directory = os.path.dirname(
    os.path.abspath(__file__))
  return os.path.join(
    script_directory, '..', filename)


