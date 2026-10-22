import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Search, Plus, Boxes, Package, TrendingUp, AlertTriangle, Pencil, Trash2, X, LoaderCircle, RefreshCw, Smartphone, Laptop, Monitor, Box } from "lucide-react";
import "./styles.css";

const API = "/api"; // Vite proxy forwards to your existing FastAPI during development
const money = n => new Intl.NumberFormat("en-IN", { style:"currency", currency:"INR", maximumFractionDigits:0 }).format(Number(n)||0);
const iconFor = name => /phone|realme|mobile/i.test(name) ? Smartphone : /laptop|hp|book/i.test(name) ? Laptop : /monitor|screen/i.test(name) ? Monitor : Box;

function App(){
  const [products,setProducts]=useState([]), [loading,setLoading]=useState(true), [error,setError]=useState("");
  const [query,setQuery]=useState(""), [modal,setModal]=useState(false), [editing,setEditing]=useState(null), [saving,setSaving]=useState(false);
  const [form,setForm]=useState({id:"",name:"",description:"",price:"",quantity:""});
  const [notice,setNotice]=useState("");
  async function load(){
    setLoading(true); setError("");
    try { const r=await fetch(`${API}/products`); if(!r.ok) throw new Error(`API returned ${r.status}`); setProducts(await r.json()); }
    catch(e){setError(`Couldn't reach the API at ${API}. Start FastAPI and check its database connection.`);}
    finally{setLoading(false);}
  }
  useEffect(()=>{load()},[]);
  const filtered=useMemo(()=>products.filter(p=>`${p.name} ${p.description} ${p.id}`.toLowerCase().includes(query.toLowerCase())),[products,query]);
  const totalValue=products.reduce((s,p)=>s+p.price*p.quantity,0), units=products.reduce((s,p)=>s+p.quantity,0), low=products.filter(p=>p.quantity<=5).length;
  function openCreate(){setEditing(null);setForm({id:"",name:"",description:"",price:"",quantity:""});setModal(true)}
  function openEdit(p){setEditing(p);setForm({id:String(p.id),name:p.name,description:p.description,price:String(p.price),quantity:String(p.quantity)});setModal(true)}
  async function save(e){
    e.preventDefault();setSaving(true);setNotice("");
    const body={id:Number(form.id),name:form.name.trim(),description:form.description.trim(),price:Number(form.price),quantity:Number(form.quantity)};
    try{
      if(!Number.isInteger(body.id)||body.id<1) throw new Error("Enter a positive whole-number product ID.");
      const r=await fetch(editing?`${API}/product?id=${encodeURIComponent(editing.id)}`:`${API}/product`,{method:editing?"PUT":"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
      if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||`Request failed (${r.status})`)}
      setModal(false);await load();setNotice(editing?"Product updated successfully":"Product added to inventory");
    }catch(e){setNotice(e.message)}finally{setSaving(false)}
  }
  async function remove(p){
    if(!confirm(`Delete “${p.name}” from inventory?`))return;
    try{const r=await fetch(`${API}/product?id=${encodeURIComponent(p.id)}`,{method:"DELETE"});if(!r.ok)throw new Error("Delete failed");await load();setNotice("Product deleted");}
    catch(e){setNotice(e.message)}
  }
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark"><Boxes size={21}/></span><span>stockroom<span className="brand-dot">.</span><small>INVENTORY STUDIO</small></span></div>
      <div className="nav-label">WORKSPACE</div><div className="nav-item active"><Package size={18}/> Inventory <span className="nav-count">{products.length}</span></div>
      <div className="sidebar-bottom"><div className="status-dot"/> API-connected workspace <small>FastAPI · PostgreSQL</small></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="eyebrow">WORKSPACE / INVENTORY</span><h1>Inventory overview</h1></div><button className="primary" onClick={openCreate}><Plus size={17}/> Add product</button></header>
      {notice&&<div className="notice" role="status">{notice}<button onClick={()=>setNotice("")}><X size={15}/></button></div>}
      {error&&<div className="error-banner"><AlertTriangle size={18}/><div><b>Backend connection issue</b><p>{error}</p></div><button className="ghost" onClick={load}><RefreshCw size={15}/> Retry</button></div>}
      <section className="stats">
        <Stat icon={Boxes} label="Products listed" value={products.length} foot="Unique items in catalog" tint="violet"/>
        <Stat icon={Package} label="Units in stock" value={units.toLocaleString("en-IN")} foot="Across all products" tint="blue"/>
        <Stat icon={TrendingUp} label="Inventory value" value={money(totalValue)} foot="Cost × available quantity" tint="green"/>
        <Stat icon={AlertTriangle} label="Low stock" value={low} foot="5 units or fewer" tint="amber"/>
      </section>
      <section className="inventory-panel">
        <div className="panel-head"><div><h2>Your products</h2><p>Manage, review and update your catalog.</p></div><div className="tools"><div className="search"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search products…"/></div><button className="icon-button" aria-label="Refresh" onClick={load}><RefreshCw size={16}/></button></div></div>
        {loading?<div className="loading"><LoaderCircle className="spin"/> Loading inventory…</div>:filtered.length===0?<div className="empty"><div className="empty-icon"><Package size={25}/></div><h3>{query?"No matching products":"Your inventory is ready"}</h3><p>{query?"Try another search term.":"Add your first item to start tracking stock."}</p>{!query&&<button className="primary" onClick={openCreate}><Plus size={16}/> Add first product</button>}</div>:
        <div className="table-wrap"><table><thead><tr><th>PRODUCT</th><th>PRICE</th><th>STOCK LEVEL</th><th>VALUE</th><th></th></tr></thead><tbody>
          {filtered.map(p=>{const Icon=iconFor(p.name);return <tr key={p.id}><td><div className="product-cell"><div className="product-icon"><Icon size={20}/></div><div><b>{p.name}</b><small>{p.description||"No description"} · ID {p.id}</small></div></div></td><td className="price">{money(p.price)}</td><td><span className={`stock ${p.quantity<=5?"low":p.quantity<=10?"medium":"healthy"}`}><i/>{p.quantity} {p.quantity===1?"unit":"units"}</span></td><td className="price">{money(p.price*p.quantity)}</td><td><div className="actions"><button title="Edit product" onClick={()=>openEdit(p)}><Pencil size={15}/></button><button title="Delete product" className="danger" onClick={()=>remove(p)}><Trash2 size={15}/></button></div></td></tr>})}
        </tbody></table></div>}
        <div className="panel-foot"><span>Showing <b>{filtered.length}</b> of <b>{products.length}</b> products</span><span className="live"><i/> Live data</span></div>
      </section>
      <footer>Stockroom <span>·</span> A simple inventory dashboard powered by your FastAPI backend.</footer>
    </main>
    {modal&&<div className="overlay" onMouseDown={e=>{if(e.target===e.currentTarget)setModal(false)}}><form className="modal" onSubmit={save}>
      <div className="modal-head"><div><span className="eyebrow">{editing?"EDIT ITEM":"NEW ITEM"}</span><h2>{editing?"Update product":"Add a product"}</h2></div><button type="button" className="icon-button" onClick={()=>setModal(false)}><X size={18}/></button></div>
      <label>Product ID<input required type="number" min="1" step="1" disabled={!!editing} value={form.id} onChange={e=>setForm({...form,id:e.target.value})} placeholder="e.g. 3"/><small>{editing?"ID cannot be changed":"Choose an unused ID; backend requires it"}</small></label>
      <label>Product name<input required maxLength="120" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="e.g. Wireless headphones"/></label>
      <label>Description<textarea maxLength="500" rows="3" value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="A short product description"/></label>
      <div className="form-row"><label>Price (₹)<input required type="number" min="0" step="0.01" value={form.price} onChange={e=>setForm({...form,price:e.target.value})} placeholder="0.00"/></label><label>Quantity<input required type="number" min="0" step="1" value={form.quantity} onChange={e=>setForm({...form,quantity:e.target.value})} placeholder="0"/></label></div>
      <div className="modal-actions"><button type="button" className="secondary" onClick={()=>setModal(false)}>Cancel</button><button className="primary" disabled={saving}>{saving?<LoaderCircle size={16} className="spin"/>:<Plus size={16}/>} {saving?"Saving…":editing?"Save changes":"Add product"}</button></div>
    </form></div>}
  </div>
}
function Stat({icon:Icon,label,value,foot,tint}){return <article className="stat-card"><div className={`stat-icon ${tint}`}><Icon size={19}/></div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-foot">{foot}</div></article>}
createRoot(document.getElementById("root")).render(<App/>);
