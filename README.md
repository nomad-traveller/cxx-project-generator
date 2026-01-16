# C/C++ Project Generator

A modern, flexible project generator for C/C++ projects using CMake and Ninja build system. Generate complete project scaffolds with libraries, executables, and optional testing framework integration.

## Features

- 🏗️ **Modern CMake**: Uses current CMake best practices with proper target management
- 🔧 **Build Configurations**: Debug and Release builds with appropriate compiler flags
- 📚 **Library Support**: Automatic library creation with proper header organization
- 🧪 **Optional Testing**: Google Test integration with automatic test discovery
- 🎯 **Flexible Configuration**: JSON-based project templates
- 🚀 **Ninja Build**: Fast, parallel builds with Ninja generator
- 📁 **Clean Structure**: Organized directory layout following C/C++ conventions

## Requirements

- Python 3.6+
- CMake 3.10+
- Ninja build system
- C/C++ compiler (GCC, Clang, MSVC)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nomad-traveller/cpp-project-generator.git
   cd cpp-project-generator
   ```

2. **Make the script executable:**
   ```bash
   chmod +x create_project.sh
   ```

3. **Generate a project:**
   ```bash
   ./create_project.sh
   ```

4. **Build the generated project:**
   ```bash
   cd ../MyProject
   cmake -B build -G Ninja
   cmake --build build
   ```

## Configuration

Edit `project_template.json` to customize your project:

```json
{
  "projectName": "MyProject",
  "outputDir": "..",
  "enableTests": true,
  "cStandard": "11",
  "cppStandard": "17",
  "libraries": [
    {
      "name": "mylib",
      "sources": ["mylib.c"],
      "headers": ["mylib.h"]
    }
  ],
  "executables": [
    {
      "name": "main",
      "sources": ["main.c"],
      "dependencies": ["mylib"]
    }
  ]
}
```

### Configuration Options

- **projectName**: Name of the generated project
- **outputDir**: Directory where project will be created (relative to script location)
- **enableTests**: Whether to include Google Test framework (`true`/`false`)
- **cStandard**: C standard version (11, 99, etc.)
- **cppStandard**: C++ standard version (17, 14, 11, etc.)
- **libraries**: Array of library definitions
- **executables**: Array of executable definitions

## Build Types

The generator supports standard CMake build types:

```bash
# Debug build (with debug symbols)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug

# Release build (optimized)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
```

## Testing

When `enableTests` is true, projects include Google Test integration:

```bash
# Build and run tests
cmake --build build
cd build
ctest

# Or run tests directly
./tests/run_tests
```

## Generated Project Structure

```
MyProject/
├── CMakeLists.txt          # Main build configuration
├── main.c                  # Main executable source
├── lib/
│   └── mylib/
│       ├── CMakeLists.txt  # Library build config
│       ├── mylib.c         # Library source
│       └── include/
│           └── mylib.h     # Public headers
└── tests/                  # Optional test directory
    ├── CMakeLists.txt      # Test build config
    └── test_mylib.cpp      # Google Test cases
```

## Examples

### Simple C Project
```json
{
  "projectName": "SimpleApp",
  "enableTests": false,
  "cStandard": "11",
  "libraries": [],
  "executables": [
    {
      "name": "app",
      "sources": ["main.c"],
      "dependencies": []
    }
  ]
}
```

### C++ Library with Tests
```json
{
  "projectName": "MathLib",
  "enableTests": true,
  "cppStandard": "17",
  "libraries": [
    {
      "name": "math",
      "sources": ["math.cpp"],
      "headers": ["math.h"]
    }
  ],
  "executables": [
    {
      "name": "calculator",
      "sources": ["main.cpp"],
      "dependencies": ["math"]
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created by [nomad-traveller](https://github.com/nomad-traveller)