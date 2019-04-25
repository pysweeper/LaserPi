function validateUsername()
{
  let username = document.forms["user"]["username"].value

  //code based on https://stackoverflow.com/questions/4434076/best-way-to-alphanumeric-check-in-javascript
  for(let i = 0; i < username.length; i++)
  {
    let code = username.charCodeAt(i)
    if (! ( (code > 47 && code < 58) || (code > 64 && code < 91) || (code > 96 && code < 123) ) )
    {
      alert("Username must be composed of purely alphanumeric characters")
      return false
    }
  }

  //all checks validated
  return true

}

