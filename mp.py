import mechanize as m

br = m.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)

response = br.open('https://www.masteringphysics.com/site/login.html')
for form in br.forms():
    print '*'*60
    print form.name
    print form
    print '*'*60

br.select_form('loginForm')
for control in br.form.controls:
    print control
    print control.type, control.name, control.value
    if control.name == 'nme':
        control.value = 'mayen@berkeley.edu'
    elif control.name == 'pwd':
        control.value = 'Munisi14@'

response = br.submit()
print response.read()
print dir(response)