# NFT_metadata_manager.py
# Python NFT Metadata Manager

A simple, command-line utility for creating, viewing, editing, and batch-generating NFT metadata JSON files for digital art and collectibles.

## 🚀 Features

* **Create New Metadata:** Generate `.json` files for individual NFTs with custom name, description, image URI, and attributes.
* **View Metadata:** Load and display the contents of any existing NFT metadata JSON file.
* **Edit Existing Metadata:** Modify core fields (name, description, image URI, external URL, background color).
* **Manage Attributes:** Add, edit, or remove `trait_type` / `value` pairs within an NFT's attributes.
* **Batch Generation:** Quickly generate a series of metadata files for a collection, leveraging a base template and sequential naming.
* **User-Friendly CLI:** Interactive command-line interface for easy navigation and management.

## 💡 How it Works

This tool is designed to manage the **off-chain metadata** for Non-Fungible Tokens (NFTs). When an NFT is minted on a blockchain (like Ethereum, Polygon, Solana, etc.), the token typically contains a pointer (a URI) to a JSON file that lives off-chain. This JSON file holds all the descriptive properties of your NFT, such as its name, description, image link, and various attributes.

**Key Concepts:**

* **JSON (JavaScript Object Notation):** The universal format for NFT metadata. This script reads and writes standard JSON files.
* **Off-Chain Data:** This manager operates entirely on your local file system. It does **NOT** interact with any blockchain or decentralized storage solutions (like IPFS, Arweave). After generating your metadata files, you would typically upload them to a content-addressed storage network (like IPFS) and then point your smart contract to those generated URIs during the minting process.
* **File Organization:** All generated and managed metadata JSON files are stored in a dedicated `metadata_files/` directory within the project.

## ⚙️ Getting Started

### Prerequisites

* Python 3.6+ installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [[https://github.com/YourUsername/python-nft-metadata-manager.git](https://github.com/Eugine1234/NFT_metadata_manager.py)](https://github.com/Eugine1234/python-nft-metadata-manager.git)
    cd python-nft-metadata-manager
    ```
    (Replace `YourUsername` with your actual GitHub username)

2.  **No external Python libraries are required.** This project uses only standard Python modules (`json`, `os`, `re`).

### Running the Manager

1.  **Open the project in VS Code.**
    ```bash
    code .
    ```
2.  **Run the script from the integrated terminal:**
    ```bash
    python nft_metadata_manager.py
    ```

## 🚀 Usage

Upon running the script, you'll be presented with a main menu in your terminal:
Create New NFT Metadata
Edit Existing NFT Metadata
View NFT Metadata
Batch Generate Metadata (for collections)
Exit

