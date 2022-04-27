const firebaseConfig = {
    apiKey: "AIzaSyDa7STz3sjnsm-jMBQ9SNlTcX7tdbmGkrA",
    authDomain: "le-loger.firebaseapp.com",
    projectId: "le-loger",
    storageBucket: "le-loger.appspot.com",
    messagingSenderId: "456284240293",
    appId: "1:456284240293:web:930e09ece1f00ba31c504c"
  };

  firebase.initializeApp(firebaseConfig);
  const auth =  firebase.auth();


  function signUp(){
    if (document.getElementById("emailr").value == "") {
        alert("Email must be filled out");
        return ;
    }
    if (document.getElementById("password-field").value == "") {
        alert("password must be filled out");
        return ;
      }
    var email = document.getElementById("emailr");
    var password = document.getElementById("password-field");

    const promise = auth.createUserWithEmailAndPassword(email.value,password.value);
    //
    promise.catch(e=>alert(e.message));
    alert("SignUp Successfully");
    window.location.href = "index.html";
  }

  //signIN function
  function  signIn(){
    if (document.getElementById("email").value == "") {
        alert("Email must be filled out");
        return ;
    }
    if (document.getElementById("password-field").value == "") {
        alert("password must be filled out");
        return ;
      }
    var email = document.getElementById("email");
    var password  = document.getElementById("password-field");
    console.log(email , password);
    const promise = auth.signInWithEmailAndPassword(email.value,password.value);
    promise.catch(e=>alert(e.message));
      
    firebase.auth().onAuthStateChanged((user)=>{
      if(user){
        window.location.href="map.html";
      }else{
        window.location.href="index.html";
      }
    })


    
  }


  //signOut

  function signOut(){
    auth.signOut();
    alert("SignOut Successfully from System");
    window.location.href = "index.html";
  }

  //active user to homepage
  function findactiveuser()
  {
    firebase.auth().onAuthStateChanged((user)=>{
        if(user){
          var email = user.email;
          alert("Active user "+email);
    
        }else{
          alert("No Active user Found")
          window.location.href = "index.html";
        }
      })
  }