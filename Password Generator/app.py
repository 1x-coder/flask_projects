# Random Password Generator Flask App

from flask import Flask,request,render_template
from datetime import date
import random
import string

#### Defining Flask App
app = Flask(__name__)


#### Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2)


@app.route('/genpassword',methods=['GET','POST'])
def genpassword():
    minpasslen = 8
    maxpasslen = 30

    passlen = int(request.form.get('passlen'))

    if passlen<minpasslen:
        return render_template('home.html',datetoday2=datetoday2,mess=f'Atleast create a {minpasslen} digit password...')

    if passlen>maxpasslen:
        return render_template('home.html',datetoday2=datetoday2,mess=f'Can Create a max {maxpasslen} digit password...')

    include_spaces = request.form.get('includespaces')
    include_numbers = request.form.get('includenumbers')
    include_special_chars = request.form.get('includespecialchars')
    include_uppercase_letters= request.form.get('includeuppercaseletters')
    
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    print(include_spaces,include_numbers,include_special_chars,include_uppercase_letters)

    char_sets = [lowercase_letters]

    # Add character sets based on the parameters
    if include_spaces=='on':
        char_sets.append(' ')
    if include_numbers=='on':
        char_sets.append(digits)
    if include_special_chars=='on':
        char_sets.append(special_chars)
    if include_uppercase_letters=='on':
        char_sets.append(uppercase_letters)

    # Combine the character sets
    all_chars = ''.join(char_sets)

    password = random.choices(all_chars, k=passlen)
    password = ''.join(password)


    return render_template('home.html',datetoday2=datetoday2,generatedpassword=password)


#### Our main function which runs the Random Password Generator Flask App
if __name__ == '__main__':
    app.run(debug=True)