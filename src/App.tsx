import React, { useEffect, useState } from "react"
import Header from "./components/Header"
import Slider from "./components/Slider"
import useStorage from "./hooks/firebase/useStorage"

const App: React.FC = () => {
  const [theme, setTheme] = useState<string>("light")
  const [timeframe, setTimeframe] = useState<number>(1)
  const [timestep, setTimestep] = useState<number>(0)

  const lightImages = useStorage("light")
  const darkImages = useStorage("dark")

  // calculate timesteps for imagery
  const timesteps = [""]
  let now = new Date(Date.now() - 15 * 60000)
  now = new Date(Math.floor(now.getTime() / (5 * 60000)) * (5 * 60000))
  for (let i=0; i<lightImages.length; i++) {
    const _timestep = new Date(now.getTime() - (i * (5 * 60000)))
    timesteps.push(_timestep.toLocaleTimeString().slice(0, -3))
  }

  const toggleMode = () => {
    theme == "dark" ? setTheme("") : setTheme("dark")
  }

  return (
    <div className={theme}>
      <div className="flex flex-col h-screen bg-white dark:bg-black">
        <Header setTimeframe={setTimeframe} toggleMode={toggleMode}/>
        <div className="flex flex-row h-5/6">
          <Slider timestep={timestep} setTimestep={setTimestep} timesteps={timesteps}/>
          <div>
            { theme == "dark" ?
              <img src={darkImages[darkImages.length-timestep-1]} className="mb-2 h-full"/>
              : <img src={lightImages[lightImages.length-timestep-1]} className="mb-2 h-full"/>
            }
          </div>
        </div>  
      </div>
    </div>
  )
}

export default App
