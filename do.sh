# Close all command prompts and open a NEW one

# Navigate to your project
cd Desktop\LogReeader

# Delete old venv
rmdir /s .venv

# Create fresh venv
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Upgrade pip FIRST (very important)
python -m pip install --upgrade pip

# Install numpy and scipy FIRST (scikit-learn depends on them)
pip install numpy==1.26.2
pip install scipy==1.11.4

# Then install scikit-learn
pip install scikit-learn==1.3.2

# Finally install the rest
pip install flask==3.0.0 pandas==2.1.4