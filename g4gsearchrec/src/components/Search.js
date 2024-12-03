import React, { useState, useEffect } from 'react';

const [results, setResults] = useState([])

useEffect(() => {
    fetch("/search").then(
        res => res.text
    )
})

export function Search() {

    return(
        <div className="sm:col-span-4">
        <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
          Email address
        </label>
        <div className="mt-2">
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          />
        </div>
      </div>
    )
}