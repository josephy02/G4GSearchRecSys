import React from 'react';

const Recommendations = ({ items }) => {
    return (
        <div className="w-full max-w-2xl mx-auto mt-8 px-4">
            <h2 className="text-xl font-semibold mb-4">Recommendations</h2>
            <ul className="space-y-4">
                {items.map((item, index) => (
                    <li 
                        key={index} 
                        className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                        <a className="text-blue-600 hover:text-blue-800 hover:underline" href={item.url}>{item.title} </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Recommendations;
