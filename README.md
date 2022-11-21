# Reading of simple captchas

## Task: 
Read an image given the following constraints:

- the number of characters remains the same each time  
- the font and spacing is the same each time  
- the background and foreground colors and texture, remain largely the same
- there is no skew in the structure of the characters.  
- the captcha generator, creates strictly 5-character captchas, and each of the characters is either an upper-case character (A-Z) or a numeral (0-9).

## Observations:
- Text is completely black, while background is grey. 
- Since font is the same, we just need a dictionary with 36 items to match to the images.

## Approach to obtain dictionary:
1. Threshold image to remove background.
2. Trim image to remove white border
3. Segment image to obtain different characters 
4. Compute Difference Hash (https://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html)
5. Dedup and label obtained images.

## Approach to read captcha:
0. Load labelled segments and compute hashes to a dictionary
1. Threshold image to remove background.
2. Trim image to remove white border
3. Segment image to obtain different characters 
4. Match with loaded dictionary.