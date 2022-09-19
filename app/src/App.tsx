import React, { useState } from "react"
import Header from "./components/Header"
import Slider from "./components/Slider"
import useStorage from "./hooks/firebase/useStorage"

const App: React.FC = () => {
  const [theme, setTheme] = useState<string>("light")
  const [timeframe, setTimeframe] = useState<number>(1)
  const [timestep, setTimestep] = useState<number>(0)

  const lightImages = useStorage("light")
  const darkImages = useStorage("dark")

  const utcOffset = 2

  // calculate timesteps for imagery
  const timesteps: string[] = []
  if (lightImages.length > 0) {
    const dateString = lightImages[lightImages.length-1].substring(85, 101)
    let date = new Date(dateString.substring(0, 4), dateString.substring(5, 7), dateString.substring(8, 10), dateString.substring(11, 13), dateString.substring(14, 16), 0)
    date = new Date(date.getTime() + utcOffset * 60 * 60000)
    for (let i=0; i<lightImages.length; i++) {
      const _timestep = new Date(date.getTime() - (i * (5 * 60000)))
      timesteps.push(_timestep.toLocaleTimeString().slice(0, -3))
    }
  }

  const toggleMode = () => {
    theme == "dark" ? setTheme("") : setTheme("dark")
  }

  const saveGif = () => {
    console.log("gif not operating yet")
  }

  return (
    <div className={theme}>
      <div className="flex flex-col h-screen bg-white dark:bg-black">
        <Header setTimeframe={setTimeframe} toggleMode={toggleMode} saveGif={saveGif}/>
        <div className="flex flex-row h-5/6">
          <Slider timestep={timestep} setTimestep={setTimestep} timesteps={timesteps}/>
          <div>
            { theme == "dark" ?
              <img src={darkImages[darkImages.length-timestep-1]} className="mt-8 mb-2 mr-2 w-full md:h-full"/>
              : <img src={lightImages[lightImages.length-timestep-1]} className="mt-8 mb-2 mr-2 w-full md:h-full"/>
            }
          </div>
        </div>  
      </div>
    </div>
  )
}

export default App
