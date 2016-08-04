import os

compiler_dir = os.path.dirname(os.path.realpath(__file__))
compilerPath = os.path.join(compiler_dir, "compiler.jar")
pngOptPath = os.path.join(compiler_dir, "pngquant.exe")
jpgOptPath = os.path.join(compiler_dir, "jpegtran.exe")
cssOptPath = "csso"
htmlOptPath = "html-minifier"