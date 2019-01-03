
<div class="container1">
  <div style="text-align:center">
    <h2>Login</h2>
  </div>
<form class='login' action="/signin" method="POST">
    <span id='mail'>E-mail :     </span><input align='left' name="email" type="mail" required /></br></br>
    <span id='password'>Password :   </span><input align='left' name="password" type="password" required /></br></br>
    <span class='err'>{{err_msg}}</span>
    <button type="login ">Submit</button>
</form>
