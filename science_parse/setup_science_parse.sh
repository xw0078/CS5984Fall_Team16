#!/usr/bin/env bash

#Change the directory to the user's home
cd ~

## Cleanup

# Delete existing installations for a fresh install.
rm -rf sbt
rm sbt-.zip
rm -rf science-parse

#Download the sbt package
echo "Downloading sbt..."
wget https://piccolo.link/sbt-1.2.4.zip

# unzip it
echo "Unzipping sbt..."
unzip sbt-1.2.4.zip

# Export the path to the sbt executable
echo "Setting up sbt..."
export PATH=$PATH:~/sbt/bin

# Load java using Arc's package management system. Sbt needs java to run
echo "Loading java/1.8.0u172 module..."
module load jdk/1.8.0u172

# Clone science parse code
echo "Cloning science-parse github repository..."
git clone https://github.com/allenai/science-parse.git

# Change directory into it
cd science-parse

# Build the science-parse fat-jar.
echo "Building the science-parse fat-jar..."
sbt cli/assembly

# After the build is complete, change the directory to the built jar file
echo "Changing directory to the fat jar."
cd cli/target/scala-2.11

# Creating a test pdf file to hide the ugly exception stack trace during execution of the next command
echo "Creating a test pdf file..."
touch test.pdf

# Trigger the parser for the first time using a dummy pdf file. It is okay if this throws error because of the wrong pdf file. We just want it to download the model files.
echo "Starting the actual science-parse setup..."
java -Xmx6g -jar science-parse-cli-assembly-2.0.2-SNAPSHOT.jar test.pdf || true # this last part makes the script run even if the first part errors out.

# removing the temporary
echo "Removing the test pdf file..."
rm test.pdf

# Change back to the user's home directory.
echo "Changing back to the user's home directory..."
cd ~

echo "Setup complete."