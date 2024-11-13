import pandas as pd
import re

weights = ['1.6kg', '0.48kg', '590g', '1.2g', '0.38g', '16x10g', '100ml', '300ml', '8 x 150g', 'MX180RYSHX']
df = pd.DataFrame({'weight': weights})

def convert_weight(value):
    try:
        value = value.lower().replace(' ', '')  # Ensure consistent formatting
        if 'kg' in value:
            return float(value.replace('kg', '').strip())  # Convert to float and assume kg
        elif 'g' in value:
            # Handle cases like '16x10g' or '8x150g'
            match = re.match(r'(\d+)[xX](\d+)g', value)
            if match:
                quantity, grams = match.groups()
                return int(quantity) * int(grams) / 1000  # Convert total grams to kg
            else:
                return float(value.replace('g', '').strip()) / 1000  # Convert grams to kg
        elif 'ml' in value:
            # Assume density of 1g/ml (i.e., 1 ml = 1 g), convert to kg
            return float(value.replace('ml', '').strip()) / 1000
        else:
            return None  # Ignore other units like ml or invalid values
    except (ValueError, AttributeError):
        return None  # Handle non-convertible values

df['weight'] = df['weight'].apply(convert_weight)
df.dropna(subset=['weight'], inplace=True)
df['weight'] = df['weight'].apply(lambda x: f"{x:.5f}kg")

print(df.to_string(index=False))
