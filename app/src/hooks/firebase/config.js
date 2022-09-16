import firebase from "firebase/compat/app"
import "firebase/compat/storage"
import "firebase/compat/firestore"

const firebaseConfig = {
  apiKey: "AIzaSyB8Yg6SL6MRtDJMvNJ0GSH-7xafPyH9Sls",
  authDomain: "beradar-fba3d.firebaseapp.com",
  projectId: "beradar-fba3d",
  storageBucket: "beradar-fba3d.appspot.com",
  messagingSenderId: "891782777995",
  appId: "1:891782777995:web:191a222a15d6272a35188e",
  measurementId: "G-FR0ZJBYHRT"
}

// Initialize Firebase
firebase.initializeApp(firebaseConfig)

const projectStorage = firebase.storage()
const projectFirestore = firebase.firestore()
const timestamp = firebase.firestore.FieldValue.serverTimestamp

export {projectStorage, projectFirestore, timestamp}