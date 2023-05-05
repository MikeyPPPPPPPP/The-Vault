# The-Vault

## I am currently rewriting the code, this code is not secure against memory forensics which is unexceptable for me.

This is a PGP encryption suite with a built in password and file manager made in Python with Tkinter


Default password:
Sixteen byte keySixteen byte key


# Why?

GPG Suite on MAC dosen't work the way I want it to.

# Features 


## PGP
  * Encryption: You can encrypt stuff with a public key
  * Decyrption: You can decrypt stuff with a private key if you add a public/private key to the password manager
  * Verification: You can verify a pgp signed message with a public key
  * Sign: You can sign stuff with a private key if you add a public/private key to the password manager

## Password Manager
   * Add password data 
   
        -- To add a password you first need to  specify a refrence that will be displayed in plaintext, from there you can add a siteurl, username, password, pin, email, phonenumber, note, public, and private number
        
   * View a password
   
        -- To view a password you need to know the refrence

## File Manager
   * Add a file
   
       -- To add a file you need to first specify a refrence number then you can pick the file you want to submit.
       
   * View a file 
   
      -- To view a file you need to picke the refrence number then you can recover, delete, or view.  Recovering the filke will write it to the current directory, and unfortenently for now you can only view image files. When viewing image files the program will read the decrypted bytes from the database so you can view the image while it is in memory if you dont want to write it to the computer.


## Options
    * Paranoid option
    
      -- This will make it so you need a password to access any tab.
