# **JASON.py 🦲 - Minimalist Json-based Database for MVPs**

Because sometimes your database needs to punch data in the face.

Meet JASON - the JSON database that's as straightforward as its namesake, Jason Statham. No fancy schemas, no complicated relationships, just pure, bald-faced data storage that gets the job done.

Like the man himself, JASON is:
- Fast and furious with your data
- Doesn't waste time with unnecessary complexity
- A safe transporter of your information (though maybe not in a fancy European car)
- Completely bald-proof (we mean fault-proof)
- Ready to kick NoSQL in the face

If your application needs a database solution that's as direct as a Statham one-liner and hits as hard as his right hook, JASON is your guy. No fancy suits, no complicated dance moves - just raw, actionable data handling with two methods - load and save!

A **minimalist, no-brainer, simple JSON-based database solution** for your MVP chatbots and apps that need NoSQL. Perfect for early-stage projects where simplicity and speed matter more than scalability. Jason is a simple json-based db solution for MVP chatbots and projects with up to 1k users and 100 concurrent users at a time. This project is early stage, so bear in mind there might be some bugs and it might not work properly.

---

## **Vision**

To provide a **lightweight, easy-to-use database solution** for MVP chatbots, allowing developers to focus on building their bot logic without worrying about database setup or maintenance when you don't really have too many users to care about scalability.

Each user should have unique User_id, which is used to access user's json. And each json has a standartized schema that was set during initialization (creation) of the database. That's it!

---

## **Conditions for Usage**

### **When to Use This Solution**
1. **MVP Stage:**
   - Perfect for early-stage chatbots where you need a quick, lightweight database solution.
   - Ideal for prototyping and testing ideas without the overhead of a full database.

2. **Small to Medium User Base:**
   - Works well for chatbots with **up to 1,000 active users**.
   - Handles **up to 100 concurrent read/write operations per second** comfortably.

3. **Simple Data Structure:**
   - Best for chatbots where each user’s data can be represented as a flat or moderately nested JSON structure.
   - Not suitable for complex relationships or queries (e.g., JOINs, transactions).

4. **Low to Moderate Write Frequency:**
   - Suitable for chatbots where user data is updated occasionally (e.g., during interactions).
   - Not ideal for high-frequency writes (e.g., logging every message).

5. **Single-Instance Deployment:**
   - Designed for single-instance deployments (e.g., one server running the bot).
   - Not suitable for distributed systems or multi-instance deployments.

---

### **When to Switch to a More Serious Solution**
1. **Large User Base:**
   - If your chatbot grows beyond **1,000 active users**, consider switching to a database like **SQLite**, **PostgreSQL**, or **MongoDB**.

2. **High Write Frequency:**
   - If you need to write data frequently, switch to a database optimized for high write throughput.

3. **Complex Queries:**
   - If you need advanced querying (e.g., filtering, sorting, aggregations), use a database with query support.

4. **Distributed Systems:**
   - If your chatbot runs on multiple instances (e.g., for scalability), switch to a distributed database like **Redis** or **Cassandra**.

5. **Data Integrity Requirements:**
   - If you need transactions, atomicity, or data consistency guarantees, use a database like **PostgreSQL**.

---

## **Features**

- **Simple:** Each user’s data is stored in a separate JSON file.
- **Async I/O:** Uses `aiofiles` for non-blocking file operations.
- **One Schema To Rule Them All:** Define a single default JSON structure for all users.
- **Atomic Writes:** Each user’s data is stored in a separate file, ensuring atomic writes.
- **Per-User Locking:** Ensures safe concurrent access using asyncio.Lock
- **orjson Serialization:** Faster than standard JSON with optional pretty-printing
- **Memory Safety:** Always returns copies of data to prevent accidental cache modification
- **Cache Coherency:** Automatic cache clearing if final save fails

---

## **Installation**

Option one: Install via pip:
   ```bash
   pip install jason-db
   ```

Option two: Download the `jason.py` file and include it in your project.

---

## **Quickstart**

1. **Initialize the Database:**
   ```python
   from jason_db import JASON

   # Define the default structure for your JSON files
   DEFAULT_STRUCTURE = {
       'challenges': {},
       'active_challenge': None,
       'challenge_balance': 0
   }

   # Initialize the DB
   db = JASON(db_folder='/path/to/db/folder', default_structure=DEFAULT_STRUCTURE)
   ```

2. **Load User Data:**
   ```python
   user_id = "12345"
   user_data = await db.load_user_data(user_id)
   print(user_data)  # Outputs the user's data or the default structure
   ```

3. **Save User Data:**
   ```python
   user_id = "12345"
   user_data = await db.load_user_data(user_id)
   user_data['challenge_balance'] += 1  # Modify data
   await db.save_user_data(user_id, user_data)
   ```

---

## **Use Cases**

1. **Telegram Bots:**
   - Store user preferences, conversation state, or game progress.
   - Example: A chatbot that tracks user challenges and balances.

2. **Prototyping:**
   - Quickly test ideas without setting up a full database.
   - Example: A proof-of-concept chatbot for a startup pitch.

3. **Small-Scale Projects:**
   - Ideal for personal projects or small teams with limited resources.
   - Example: A hobby project to learn chatbot development.

---

## **Limitations**

- **Not for Large-Scale Systems:** Use for up to 1,000 active users, maybe 10,000 in some cases tops.
- **No Advanced Queries:** Only supports basic read/write operations.
- **Single-Instance Only:** Not suitable for distributed deployments.

---

## **When to Upgrade**

If your chatbot grows beyond 1,000-10,000 users or requires advanced features like transactions, consider switching to:

- **SQLite** for a lightweight SQL database.
- **PostgreSQL** for a robust relational database.
- **MongoDB** for a NoSQL database with flexible schemas.

---

## **Contributing**

Feel free to open issues or submit pull requests! This project is open-source and welcomes contributions.

---

## **License**

MIT License. Use it freely for personal and commercial projects.
