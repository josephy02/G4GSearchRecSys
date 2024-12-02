import React from 'react';

const Recommendations = ({ items }) => {
    return (
        <div>
            <h2>Recommendations</h2>
            <ul>
                {items.map((item, index) => (
                    <li key={index}>
                        <a href={item.url}>{item.title}</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Recommendations;
