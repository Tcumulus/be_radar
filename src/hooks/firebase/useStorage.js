import { useState, useEffect } from "react"
import { projectStorage } from "../firebase/config"

const useStorage = (mode) => {
  const [files, setFiles] = useState([])

  useEffect(() => {
    const fetchImages = async () => {
      const result = await projectStorage.ref(mode).listAll()
      const urlPromises = result.items.map(imageRef => imageRef.getDownloadURL())
      return Promise.all(urlPromises)
    }
    
    const loadImages = async () => {
      const urls = await fetchImages()
      setFiles(urls)
    }
    loadImages()
  }, [])

  return files
}

export default useStorage