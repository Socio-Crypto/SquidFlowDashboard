# SquidFlowVisualizer

## Objective

The primary objective of this dashboard is to furnish a comprehensive and insightful analytical overview of the interchain bridge Squid. Squid's pivotal function revolves around facilitating frictionless token swaps among various blockchains, thereby simplifying the process of accessing applications across disparate chains through a single, user-friendly interface.

Empowered by Squid's robust API and versatile SDK, developers gain the capability to seamlessly orchestrate token swaps across diverse blockchain environments. This functionality extends to enabling the linkage of multiple swaps and on-chain function calls across an extensive array of integrated chains. This innovative capacity empowers users to instantaneously traverse novel ecosystems, thereby unlocking the untapped potential harbored within different chains.

Squid currently supports bridging across an impressive spectrum of 13 chains: Ethereum, Arbitrum, Optimism, Polygon, Avalanche, Binance, Fantom, Moonbeam, Celo, Base, Linea, Filecoin, and Kava. By deploying a network of decentralized exchanges (DEXes), Squid seamlessly facilitates cross-chain swaps, fostering interoperability and fluid asset movement between the aforementioned chains and various others.

The analytics section of this dashboard serves as an insightful visualization tool, elucidating the intricate flow of assets through Squid's interchain mechanism. The network topology depicted therein provides a lucid illustration of how Squid effectively interconnects distinct chains, akin to nodes within a network. Users can further delve into a wealth of analysis specific to individual wallet addresses by utilizing the search function situated above.

Complementing this, the leaderboard tab enhances the user experience by offering an at-a-glance summary of active users and prominent decentralized exchanges (DEXes) within the Squid ecosystem. This multifaceted dashboard empowers users with the insights needed to navigate the interchain landscape and capitalize on its potential.

## Method and Data

Interoperability has emerged as a prominent trend driven by genuine needs within the blockchain ecosystem, encompassing seamless interchain communication and secure movement of assets across chains. While interoperability offers novel opportunities, it also introduces fresh challenges. Within the realm of blockchain analytics, achieving interoperability necessitates tapping into diverse data sources. Recognizing the inherent limitations of data-sharing platforms, especially concerning interchain protocol analytics, a multi-faceted approach becomes essential. The comprehensive analysis of interchain protocols demands the integration of data from multiple sources, encompassing all relevant chains.

Our dashboard addresses these complexities by amalgamating the Graph data and Flipside data, enabling a comprehensive visualization of asset flows through Squid across a multitude of chains. Squid, currently, supports asset origins across 13 distinct chains. In this iteration of the Squid Flow Visualizer, we leverage Flipside's data for 7 chains, while the Graph SDK augments our analysis with data from 3 additional chains.

To harness Flipside's capabilities, we have seamlessly integrated SQL queries into our codebase, which can be readily accessed on our GitHub repository. These queries empower the extraction of valuable insights from Flipside's SDK. Correspondingly, the SQL code is available via the following link (link).

Furthermore, our methodology encompasses the utilization of three subgraphs for analyzing data from Fantom, Celo, and Moonbeam chains. These subgraphs, collaboratively developed with KIDACRYPTO, bolster the accuracy and depth of our analysis.

The integration of data from Flipside SDK and Graph SDK underpins our analytical framework. By merging these datasets, we synergistically harness their capabilities, enriching the depth and precision of our analyses.

## Roadmap

The current iteration of the Squid Flow Visualizer encompasses the visualization of 8 out of the 13 chains that Squid supports. In the near future, we anticipate the inclusion of data for the remaining chains, namely Base and Optimism, pending the integration of data from Flipside into our tables. Looking ahead, our strategic vision involves augmenting the analytical capacity of the platform by incorporating Bitquery data, thereby expanding the scope to encompass Filecoin. For two other chains, we intend to integrate data from alternative sources, broadening our data stream.

As we embark on the next phase of development, we are excited to introduce a dedicated tab exclusively focused on delivering a comprehensive analysis of Squid users and their activities. This forthcoming enhancement promises to provide valuable insights into user behavior and engagement within the Squid ecosystem. We are diligently working to bring this enhanced version to fruition, with an anticipated release in just two weeks.

Our commitment to continuous improvement remains unwavering, and these developments mark the beginning of an exciting journey towards a more enriched and insightful Squid Flow Visualizer. Stay tuned for these exciting updates as we strive to enhance the functionality and value of our platform.
