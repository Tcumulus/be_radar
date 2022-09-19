import React from "react"

interface Props {
  timestep: number,
  setTimestep: (value: number) => void,
  timesteps: string[]
}

const Slider: React.FC<Props> = ({ timestep, setTimestep, timesteps }) => {
  return (
    <div className="flex flex-col items-center w-1/5 m-4 md:mr-16">
      <p className="h-fit font-bold m-4 text-xl md:text-2xl p-2 md:p-4 md:px-8 text-gray-600 dark:text-gray-300 bg-white dark:bg-black shadow-sm border rounded-xl">
        {timesteps[timestep]}
      </p>
      <div className="flex flex-col items-center w-full ">
        {
          timesteps.map((item, index) => {
            return <p onMouseEnter={() => setTimestep(index)} key={item} className="px-1 text-gray-600 dark:text-gray-300 hover:font-bold cursor-pointer">{item}</p>
          })
        }
      </div>
    </div>
  )
}

export default Slider