import React from "react"

interface Props {
  setTimeframe: (param: number) => void,
  toggleMode: () => void,
  saveGif: () => void
}

const Header: React.FC<Props> = ({ setTimeframe, toggleMode, saveGif }) => {
  return (
    <div className="flex flex-row justify-between mb-4 items-center">
      <h1 className="m-4 ml-8 text-3xl text-gray-600 dark:text-gray-300 font-medium">Radar Belgium</h1>
      <div className="flex flex-row flex-grow justify-end">
        <select defaultValue="1h" className="h-fit m-4 p-2 text-gray-600 dark:text-gray-100 bg-white dark:bg-black shadow-sm border rounded-md outline-none">
            <option value="30m" onClick={() => setTimeframe(0.5)}>30mins</option>
            <option value="1h" onClick={() => setTimeframe(1)}>1h</option>
            <option value="2h" onClick={() => setTimeframe(2)}>2h</option>
        </select>
        <div className="h-fit flex flex-row items-center m-4 p-2 text-gray-600 dark:text-gray-300 bg-white dark:bg-black shadow-sm border rounded-md outline-none">
          <input type="checkbox" onClick={toggleMode} className="w-4 h-4 outline-none"/>
          <p className="h-fit ml-2 text-gray-600 dark:text-gray-300">Dark Mode</p>
        </div>
        <button className="h-fit ml-2 m-4 p-2 text-gray-600 dark:text-gray-300 bg-white dark:bg-black shadow-sm border rounded-md">Save GIF</button>
      </div>
    </div>
  )
}

export default Header
