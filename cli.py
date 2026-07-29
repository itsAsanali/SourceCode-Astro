import sys
import os
from lexer import AstroLexer
from parser import AstroParser
from codegen import AstroCodeGenerator

def print_help():
    print("Astro Compiler CLI v1.0.0")
    print("Usage: astro <file.ast | file.astro> [-o output.js]")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_help()
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = None

    if len(sys.argv) >= 4 and sys.argv[2] == "-o":
        output_file = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + ".js"

    with open(input_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    try:
        lexer = AstroLexer(source_code)
        tokens = lexer.tokenize()

        parser = AstroParser(tokens)
        ast = parser.parse_component()

        generator = AstroCodeGenerator(ast)
        compiled_js = generator.generate_js()

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(compiled_js)

        print(f"[Astro] Successfully compiled '{input_file}' -> '{output_file}'")
    except Exception as e:
        print(f"[Astro Error]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()